from abc import ABC, abstractmethod
from convomerge.state import TriggerPlaceholder
from convomerge.path import LinearScriptPath
from convomerge.matchers import ActionMatcher, TriggerValueMatcher


class PathMergeResult:
    def __init__(self, base_path: LinearScriptPath, merge_path: LinearScriptPath, merged_states_mapping: dict[str, str]) -> None:
        self.base_path = base_path
        self.merge_path = merge_path
        self.merged_states_mapping = merged_states_mapping

    def __repr__(self) -> str:
        return f'PathMergeResult(base_path={repr(self.base_path)}, merge_path={repr(self.merge_path)}, merged_states_mapping={repr(self.merged_states_mapping)})'


class PathMergeStrategy(ABC):
    @abstractmethod
    def merge(self, base: LinearScriptPath, other: LinearScriptPath) -> PathMergeResult:
        pass


class BackPropagationPathMergeStrategy(PathMergeStrategy):
    def __init__(self, action_comparator: ActionMatcher, trigger_comparator: TriggerValueMatcher) -> None:
        super().__init__()
        self._action_comparator = action_comparator
        self._trigger_comparator = trigger_comparator

    def merge(self, base: LinearScriptPath, other: LinearScriptPath) -> PathMergeResult:
        merge_path = LinearScriptPath()
        merged_states_mapping = {}

        base_reversed = list(base.iter_states())
        base_reversed.reverse()
        other_reversed = list(other.iter_states())
        other_reversed.reverse()

        for base_state in base_reversed: 
            state_until_merge_counter = 0

            for other_state in other_reversed:
                state_until_merge_counter += 1

                if not self._action_comparator.match_seq(base_state.actions, other_state.actions):
                    continue
                
                if len(base_state.triggers) == len(other_state.triggers) == 0:
                    # Merge point found
                    break
                
                base_state_trigger, other_state_trigger = base_state.triggers[0], other_state.triggers[0]

                if not base_state_trigger.is_next() and not other_state_trigger.is_next():
                    # Merge point found
                    break
                
                if merged_states_mapping[merge_path.get_first_state().name] == base_state_trigger.state_name:
                    # Merge point found
                    break
            else:
                continue

            other_merge_slice = other_reversed[:state_until_merge_counter]
            other_reversed = other_reversed[state_until_merge_counter:]

            # Add merge slice to merge results
            for other_state in other_merge_slice:
                if len(other_state.triggers) == 0:
                    merge_path.prepend_state(other_state.actions, TriggerPlaceholder.default())
                else:
                    merge_path.prepend_state(other_state.actions, TriggerPlaceholder.from_trigger(other_state.triggers[0]))

            merged_states_mapping[merge_path.get_first_state().name] = base_state.name

        return PathMergeResult(base, merge_path, merged_states_mapping)
    
