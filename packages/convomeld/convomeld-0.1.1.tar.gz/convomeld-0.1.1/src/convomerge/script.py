from __future__ import annotations
from typing import Optional, TextIO, Union, Any
from collections.abc import Sequence
from convomerge.state import Action, State, Trigger, TriggerPlaceholder
from convomerge.path import LinearScriptPath
from convomerge.parsers import ScriptParser, SimpleScriptParser
from convomerge.matchers import ActionMatcher, SimpleActionComparator, TriggerValueMatcher, SimpleTriggerValueMatcher
from convomerge.mergers import PathMergeStrategy, BackPropagationPathMergeStrategy, PathMergeResult
import os
import yaml
from uuid import uuid4


class Script:
    def __init__(
        self, 
        states: Optional[dict[str, State]] = None, 
        action_comparator: Optional[ActionMatcher] = None,
        trigger_comparator: Optional[TriggerValueMatcher] = None,
        merge_strategy: Optional[PathMergeStrategy] = None,
        convo_name: Optional[str] = None,
        convo_description: Optional[str] = None
    ) -> None:
        if states is None:
            if convo_name is None:
                raise RuntimeError('convo_name must be provided')
            if convo_description is None:
                convo_description = ''

            self._states: dict[str, State] = {
                'start': State('start', triggers=[TriggerPlaceholder.next().create_trigger('stop')], convo_name=convo_name, convo_description=convo_description),
                'stop': State('stop')
            }
            # self._max_level = 0
        else:
            self._states: dict[str, State] = {state_name: state.copy() for state_name, state in states.items()}
            # self._max_level = max([state.kwargs.get('level', 0) for state in self._states.values()])
        
        self._start_state: State = self._states['start']
        self._current_state: State = self._start_state
        self._stop_state: State = self._states['stop']

        self._action_comparator = action_comparator or SimpleActionComparator()
        self._trigger_comparator = trigger_comparator or SimpleTriggerValueMatcher()
        self._merge_strategy = merge_strategy or BackPropagationPathMergeStrategy(self._action_comparator, self._trigger_comparator)
        self._uuid = uuid4().hex[-6:]
        self._state_count = 0

    # Graph section

    def _find_state(
        self,
        name: Optional[str]=None,
        actions: Optional[Sequence[Action]]=None,
        many: bool=False
    ) -> Optional[State] | Sequence[State]:
        if name is not None:
            states = [self._states[name]] if name in self._states else []
        else:
            states = list(self._states.values())

        if actions is not None:
            states = [state for state in states if self._action_comparator.match_seq(state.actions, actions)]

        if many:
            return states
        else:
            return states[0] if len(states) else None
        
    def _find_paths(self, from_state: State, to_state: Optional[State], many: bool = False) -> Union[LinearScriptPath, list[LinearScriptPath]]:
        states_queue: list[tuple[State, LinearScriptPath]] = [
            (from_state, LinearScriptPath().append_state(from_state.actions, TriggerPlaceholder.empty()))
        ]
        processed_states = set()
        discovered_paths = []

        while len(states_queue) > 0:
            current_state, current_path = states_queue.pop(0)

            if current_state is to_state and current_path.num_triggers() > 0:
                if not many:
                    return current_path
                
                discovered_paths.append(current_path)

                if current_state.find_trigger(TriggerPlaceholder.default().create_trigger(current_state.name), self._trigger_comparator):
                    discovered_paths.append(current_path.copy().append_state(current_state.actions, TriggerPlaceholder.default()))

                continue
            if current_state in processed_states:
                if to_state is None:
                    discovered_paths.append(current_path)

                continue

            processed_states.add(current_state)
            next_states = [
                self._find_state(name=trigger.state_name) 
                for trigger in current_state.triggers
            ]
            next_paths = [
                current_path.copy().append_state(next_state.actions, TriggerPlaceholder.from_trigger(trigger)) 
                for next_state, trigger in zip(next_states, current_state.triggers)
            ]
            states_queue += zip(next_states, next_paths)

        return discovered_paths
    
    def append_state(self, actions: list[Action], tp: TriggerPlaceholder, **state_kwargs: dict[str, Any]) -> None:
        if self._current_state is self._start_state:
            tp = TriggerPlaceholder.next()

        self._state_count += 1
        new_state = State(f'script_{self._uuid}/state_{self._state_count}', actions, **state_kwargs)
        self._states[new_state.name] = new_state
        self._current_state.triggers.append(tp.create_trigger(new_state.name))
        self._current_state = new_state

    def move_to_state(self, state_name: str, tp: TriggerPlaceholder, **state_kwargs: dict[str, Any]) -> None:
        if state_name not in self._states:
            raise RuntimeError(f'State name error: target state name "{state_name}" not found in {list(self._states.keys())}')
        
        state = self._states[state_name]
        state.kwargs.update(state_kwargs)
        self._current_state.triggers.append(tp.create_trigger(state_name))
        self._current_state = state

    def merge_or_append_branch(self, branch: LinearScriptPath, tp: TriggerPlaceholder, mark_stop: bool = False) -> None:
        # Remove stop trigger from current state
        stop_trigger = None
        for trigger in self._current_state.triggers:
            if trigger.state_name == 'stop':
                stop_trigger = trigger.copy()
                break
        else:
            raise RuntimeError('Stop trigger not found in current state')
        
        self._current_state.remove_trigger(trigger, self._trigger_comparator)
    
        if branch.num_states() == 0:
            stop_trigger = tp.create_trigger('stop')
        elif self.try_merge_branch(branch, tp):
            stop_trigger = TriggerPlaceholder.none().create_trigger('stop')
        else:
            self.append_branch(branch, tp, mark_stop)
            stop_trigger = TriggerPlaceholder.next().create_trigger('stop')
        
        self._current_state.triggers.append(stop_trigger)
    
    def try_merge_branch(self, branch: LinearScriptPath, tp: TriggerPlaceholder) -> bool:
        extended_branch = (LinearScriptPath()
                .append_state(self._current_state.actions, TriggerPlaceholder.empty())
                .append_path(branch, tp))

        merge_result = self._find_optimal_merge_path(extended_branch)
        if merge_result is None:
            return False

        self._perform_merge(merge_result)
        return True

    def append_branch(self, branch: LinearScriptPath, tp: TriggerPlaceholder, mark_stop: bool = False) -> None:
        for state, prev_trigger in branch.iter_states(with_prev_trigger=True):
            state_tp = tp if prev_trigger is None else TriggerPlaceholder.from_trigger(prev_trigger)
            self.append_state(state.actions, state_tp, **state.kwargs)

        if mark_stop:
            return self
        
        # Create loopback
        loopback_trigger = TriggerPlaceholder.default().create_trigger(self._current_state.name)
        if self._current_state.find_trigger(loopback_trigger, self._trigger_comparator) is None:
            self._current_state.triggers.append(loopback_trigger)

        return self

    def _find_optimal_merge_path(self, branch: LinearScriptPath) -> Optional[PathMergeResult]:
        potential_merge_points = self._find_state(actions=branch.get_last_state().actions, many=True)
        best_merge_result = None

        for merge_point in potential_merge_points:
            potential_merge_paths = self._find_paths(self._current_state, merge_point, many=True)

            for base_path in potential_merge_paths:
                merge_result = self._merge_strategy.merge(base_path, branch)

                if best_merge_result is None or len(merge_result.merged_states_mapping) > len(best_merge_result.merged_states_mapping):
                    best_merge_result = merge_result
        
        return best_merge_result
    
    def _perform_merge(self, merge_result: PathMergeResult):
        current_base_state = self._current_state
        base_state = merge_result.base_path.pop_first_state()

        for state, prev_trigger in merge_result.merge_path.iter_states(with_prev_trigger=True):
            if state.name not in merge_result.merged_states_mapping:
                # The state is not in base path (existing part of script) and should be appended
                self.append_state(state.actions, TriggerPlaceholder.from_trigger(prev_trigger), **state.kwargs)
            else:
                # The state should be merged to existing state

                while base_state.name != merge_result.merged_states_mapping[state.name]:
                    current_base_trigger = current_base_state.find_trigger(TriggerPlaceholder.from_trigger(base_state.triggers[0]), self._trigger_comparator)
                    current_base_state = self._states[current_base_trigger.state_name]
                    current_base_state.kwargs.update(base_state.kwargs)
                    base_state = merge_result.base_path.pop_first_state()
                
                if prev_trigger is not None:
                    self.move_to_state(current_base_state.name, TriggerPlaceholder.from_trigger(prev_trigger), **base_state.kwargs)

    # Export section

    def to_list(self) -> list:
        return [state.to_dict() for state in self._states.values()]
    
    def to_yaml(self, fp: str | TextIO) -> None:
        if isinstance(fp, str):
            if not fp.endswith('.yml') :
                fp += '.yml'
            dir = os.path.dirname(fp)
            if not os.path.exists(dir):
                os.makedirs(dir)
            fp = open(fp, 'w', encoding='utf-8')

        script_list = self.to_list()
        yaml.safe_dump(script_list, fp, sort_keys=False, encoding='utf-8')
        fp.close()

    # Import section

    @classmethod
    def from_list(cls, states_list: list) -> Script:
        states = {
            state_dict['name']: State.from_dict(state_dict)
            for state_dict in states_list
        }

        script = cls(states=states)
        return script

    @classmethod
    def from_file(
        cls, 
        fp: str | TextIO, 
        text_script_parser: Optional[ScriptParser] = None, 
        action_comparator: Optional[ActionMatcher] = None,
        convo_name: Optional[str] = None,
        convo_description: Optional[str] = None,
        base_author: str = 'teacher'
    ) -> Script:
        if isinstance(fp, str) and (fp.endswith('.yml') or fp.endswith('.yaml')):
            return cls.from_yaml_file(fp)
        else:
            # Assume text file by default
            if text_script_parser is None:
                text_script_parser = SimpleScriptParser()
            if action_comparator is None:
                action_comparator = SimpleActionComparator()
            if convo_name is None:
                convo_name = 'convo_name'
            if convo_description is None:
                convo_description = ''

            return cls.from_text_file(fp, text_script_parser, action_comparator, convo_name, convo_description, base_author)
        
    @classmethod
    def from_yaml_file(cls, fp: str | TextIO):
        if isinstance(fp, str): 
            fp = open(fp, 'r', encoding='utf-8')

        script_list = yaml.safe_load(fp)
        fp.close()
        return cls.from_list(script_list)
    
    @classmethod
    def from_text_file(
        cls, 
        fp: str | TextIO, 
        text_script_parser: ScriptParser, 
        action_comparator: ActionMatcher,
        convo_name: str,
        convo_description: str,
        base_author: str
    ) -> Script:
        if isinstance(fp, str): 
            fp = open(fp, encoding='utf-8')

        raw_lines = fp.readlines()
        fp.close()

        # Build script
        script = cls(action_comparator=action_comparator, convo_name=convo_name, convo_description=convo_description)
        branch = LinearScriptPath()
        tp = TriggerPlaceholder.next()
        script_lines = text_script_parser.parse_lines(raw_lines)

        for line in script_lines:
            if line.author == base_author:
                action = Action(line.text, line.lang_group)
                branch.append_state(action, TriggerPlaceholder.next())
            else:
                script.merge_or_append_branch(branch, tp)
                branch = LinearScriptPath()
                tp = TriggerPlaceholder(line.text, line.lang_group)

        script.merge_or_append_branch(branch, tp, mark_stop=True)

        return script


def read_file(
    fp: str | TextIO, 
    text_script_parser: Optional[ScriptParser] = None, 
    action_comparator: Optional[ActionMatcher] = None,
    convo_name: Optional[str] = None,
    convo_description: Optional[str] = None,
    base_author: str = 'teacher',
) -> Script:
    return Script.from_file(
        fp, 
        text_script_parser=text_script_parser, 
        action_comparator=action_comparator, 
        convo_name=convo_name,
        convo_description=convo_description,
        base_author=base_author
    )