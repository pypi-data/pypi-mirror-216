from abc import ABC, abstractmethod
from collections.abc import Sequence
import re


class ScriptLine:
    def __init__(self, text: str, author: str, lang_group: str) -> None:
        self.text = text
        self.author = author
        self.lang_group = lang_group

    def __repr__(self) -> str:
        return f"ScriptLine(text='{self.text}', author='{self.author}', lang_group='{self.lang_group}')"


class ScriptParser(ABC):
    @abstractmethod
    def parse_lines(self, raw_lines: Sequence[str]) -> Sequence[ScriptLine]:
        pass


class SimpleScriptParser(ScriptParser):
    def __init__(self, parse_line_regex: str = None, collapse_lines: bool = False) -> None:
        super().__init__()
        
        if parse_line_regex is None:
            parse_line_regex = '(?P<author>\w+):\s(?P<text>.+)'

        self.parse_line_pattern = re.compile(parse_line_regex)
        self.collapse_lines = collapse_lines
        self.default_lang_group = 'en'

    def parse_lines(self, raw_lines: Sequence[str]) -> Sequence[ScriptLine]:
        if self.collapse_lines:
            return self._parse_lines_with_collapse(raw_lines)
        else:
            return self._parse_lines_without_collapse(raw_lines )

    def _parse_lines_with_collapse(self, raw_lines: Sequence[str]) -> Sequence[ScriptLine]:
        # Collapses (combines) sequential lines from the same author into single line
        dialogue_lines = []
        current_line = None

        if len(raw_lines) == 0:
            return []

        for raw_line in raw_lines:
            new_line = self._parse_raw_line(raw_line)
            
            if current_line is None:
                current_line = new_line
            elif new_line.author == current_line.author:
                current_line.text += '\n' + new_line.text
            else:
                dialogue_lines.append(current_line)
                current_line = new_line

        dialogue_lines.append(current_line)
        return dialogue_lines

    def _parse_lines_without_collapse(self, raw_lines: Sequence[str]) -> Sequence[ScriptLine]:
        # Doesn't combine sequential lines from the same author into single line
        dialogue_lines = [self._parse_raw_line(line) for line in raw_lines]
        return dialogue_lines

    def _parse_raw_line(self, line: str) -> ScriptLine:
        match = self.parse_line_pattern.match(line)
        line = ScriptLine(text=match.group('text'), author=match.group('author'), lang_group=self.default_lang_group)
        return line