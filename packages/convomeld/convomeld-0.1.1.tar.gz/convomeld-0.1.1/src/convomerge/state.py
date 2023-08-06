from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union

if TYPE_CHECKING:
    from convomerge.matchers import TriggerValueMatcher


class Action:
    def __init__(self, value: str, group_name: str) -> None:
        self.value = value
        self.group_name = group_name

    def __repr__(self) -> str:
        return f'Action(value={repr(self.value)}, group_name={repr(self.group_name)})'
    
    def copy(self, value: Optional[str] = None, group_name: Optional[str] = None) -> Action:
        if value is None:
            value = self.value
        if group_name is None:
            group_name = self.group_name

        return Action(value, group_name)


class Trigger:
    value_default = '__default__'
    value_next = '__next__'
    value_empty = ''
    value_none = None

    default_group_name = 'en'

    def __init__(self, value: str, state_name: str, group_name: str) -> None:
        self.value = value
        self.state_name = state_name
        self.group_name = group_name

    def __repr__(self) -> str:
        return f'Trigger(value={repr(self.value)}, state_name={repr(self.state_name)}, group_name={repr(self.group_name)})'
    
    def copy(self, value: Optional[str] = None, state_name: Optional[str] = None, group_name: Optional[str] = None) -> Trigger:
        if value is None:
            value = self.value
        if state_name is None:
            state_name = self.state_name
        if group_name is None:
            group_name = self.group_name

        return Trigger(value, state_name, group_name)
    
    def is_default(self) -> bool:
        return self.value == Trigger.value_default

    def is_next(self) -> bool:
        return self.value == Trigger.value_next
    
    @classmethod
    def default(cls, state_name: str) -> Trigger:
        return cls(cls.value_default, state_name, cls.default_group_name)
    
    @classmethod
    def next(cls, state_name: str) -> Trigger:
        return cls(cls.value_next, state_name, cls.default_group_name)


class TriggerPlaceholder:
    def __init__(self, value: str, group_name: str) -> None:
        self.value = value
        self.group_name = group_name

    def __repr__(self) -> str:
        return f'TriggerPlaceholder(value={repr(self.value)}, group_name={repr(self.group_name)})'

    def create_trigger(self, state_name: str):
        if self.value == Trigger.value_empty:
            raise RuntimeError('Empty trigger placeholder cannot be used to instantiate trigger')
        
        return Trigger(self.value, state_name, self.group_name)
    
    @classmethod
    def empty(cls) -> TriggerPlaceholder:
        return cls(Trigger.value_empty, Trigger.default_group_name)
    
    @classmethod
    def none(cls) -> TriggerPlaceholder:
        return cls(Trigger.value_none, Trigger.default_group_name)

    @classmethod
    def default(cls) -> TriggerPlaceholder:
        return cls(Trigger.value_default, Trigger.default_group_name)
    
    @classmethod
    def next(cls) -> TriggerPlaceholder:
        return cls(Trigger.value_next, Trigger.default_group_name)
    
    @classmethod
    def from_trigger(cls, trigger: Trigger) -> TriggerPlaceholder:
        return cls(trigger.value, trigger.group_name)


class State:
    def __init__(self, name: str, actions: Optional[list[Action]] = None, triggers: Optional[list[Trigger]] = None, **kwargs) -> None:
        self.name = name
        self.kwargs = kwargs

        if actions is None:
            self.actions: list[Action] = []
        else:
            self.actions: list[Action] = [action.copy() for action in actions]

        if triggers is None:
            self.triggers: list[Trigger] = []
        else:
            self.triggers: list[Trigger] = [trigger.copy() for trigger in triggers]
        
    def __repr__(self) -> str:
        return f'State(name={repr(self.name)}, actions={repr(self.actions)}, triggers={repr(self.triggers)}, **{repr(self.kwargs)})'
    
    def __str__(self) -> str:
        return f'State("{" ".join(map(lambda a: a.value, self.actions))}", name={self.name})'
    
    def copy(self, name: Optional[str] = None, actions: Optional[list[Action]] = None, triggers: Optional[list[Trigger]] = None, **kwargs) -> State:
        if name is None:
            name = self.name
        if actions is None:
            actions = self.actions
        if triggers is None:
            triggers = self.triggers

        kwargs = {**self.kwargs, **kwargs}

        new_state = State(name, **kwargs)
        new_state.actions =  [action.copy() for action in actions]
        new_state.triggers = [trigger.copy() for trigger in triggers]
        return new_state
    
    def find_trigger(self, target: Union[Trigger, TriggerPlaceholder], comparator: TriggerValueMatcher, index: bool = False) -> Optional[Union[Trigger, int]]:
        if isinstance(target, Trigger):
            target_value = target.value
            target_group_name = target.group_name
            target_state_name = target.state_name
        elif isinstance(target, TriggerPlaceholder):
            target_value = target.value
            target_group_name = target.group_name
            target_state_name = None

        for i, trigger in enumerate(self.triggers):
            if (
                trigger.group_name == target_group_name
                and (
                    trigger.value == target_value
                    or comparator.match(trigger.value, target_value)
                )
            ):
                if target_state_name is not None and trigger.state_name != target_state_name:
                    raise RuntimeError('Inconsistent state name for trigger')
                
                if index:
                    return i
                else:
                    return trigger.copy()
            
        return None
    
    def remove_trigger(self, target: Union[Trigger, TriggerPlaceholder], comparator: TriggerValueMatcher) -> Optional[Trigger]:
        index = self.find_trigger(target, comparator, index=True)        
        return self.triggers.pop(index).copy() if index is not None else None
    
    # Export section

    def to_dict(self) -> dict:
        state_dict = {
            'name': self.name,
            **self.kwargs,
        }

        if len(self.actions):
            actions_dict: dict[str, list[str]] = {}

            for action in self.actions:
                actions_dict.setdefault(action.group_name, [])
                actions_dict[action.group_name].append(action.value)

            state_dict['actions'] = actions_dict
        
        if len(self.triggers):
            triggers_dict: dict[str, dict[str, str]] = {}

            for trigger in self.triggers:
                triggers_dict.setdefault(trigger.group_name, {})
                triggers_dict[trigger.group_name][trigger.value] = trigger.state_name

            state_dict['triggers'] = triggers_dict

        return state_dict
    
    # Import section

    @classmethod
    def from_dict(cls, state_dict: dict) -> State:
        actions = state_dict.pop('actions', {})
        triggers = state_dict.pop('triggers', {})

        state = cls(name=state_dict.pop('name'), **state_dict)
            
        for action_group_name, action_group in actions.items():
            for action_value in action_group:
                state.actions.append(Action(action_value, action_group_name))
        
        for trigger_group_name, trigger_group in triggers.items():
            for trigger_value, next_state_name in trigger_group.items():
                state.triggers.append(Trigger(trigger_value, next_state_name, trigger_group_name))
            
        return state