from abc import ABC, abstractmethod
from collections.abc import Sequence
from convomerge.state import Action, Trigger


class ActionMatcher(ABC):
    @abstractmethod
    def match(self, action1: Action, action2: Action) -> bool:
        pass

    def match_seq(self, action_seq1: Sequence[Action], action_seq2: Sequence[Action]):
        if len(action_seq1) != len(action_seq2):
            return False
        
        for action1, action2 in zip(action_seq1, action_seq2):
            if not self.match(action1, action2):
                return False
            
        return True


class SimpleActionComparator(ActionMatcher):
    def match(self, action1: Action, action2: Action) -> bool:
        return action1.group_name == action2.group_name and action1.value == action2.value


class TriggerValueMatcher(ABC):
    @abstractmethod
    def match(self, trigger_value1: str, trigger_value2: str):
        pass


class SimpleTriggerValueMatcher(TriggerValueMatcher):
    def match(self, trigger_value1: str, trigger_value2: str):
        return str(trigger_value1) == str(trigger_value2)