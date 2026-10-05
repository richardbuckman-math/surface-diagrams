"""State and checked browser actions for the boundary-twist playground."""

from dataclasses import asdict

from .boundary_playground import import_project, new_project
from .boundary_playground_geometry import (
    braid_svg, factorization_svg, row_height, support_svg,
)


SESSION_FORMAT = 'surface-diagrams-boundary-session-v1'
MAX_HISTORY = 60


class BoundaryLab:
    """Keep undo history separate from the older six-point (6,7) lab."""

    def __init__(self):
        self.history = [new_project(3, 1)]
        self.operations = ['Three-point boundary twist']
        self.position = 0
        self.revision = 0
        self.message = 'Choose a twist, then split and move its factors.'

    @property
    def project(self):
        return self.history[self.position]

    def session_document(self):
        return {
            'format': SESSION_FORMAT,
            'history': [project.to_dict() for project in self.history],
            'operations': list(self.operations),
            'position': self.position,
        }

    def restore(self, document):
        """Validate a complete saved history before replacing the current one."""
        if not isinstance(document, dict) or document.get('format') != SESSION_FORMAT:
            raise ValueError('Not a boundary playground session')
        rows = document.get('history')
        labels = document.get('operations')
        position = document.get('position')
        if (not isinstance(rows, list) or not 1 <= len(rows) <= MAX_HISTORY or
                not isinstance(labels, list) or len(labels) != len(rows) or
                any(not isinstance(label, str) or not 1 <= len(label) <= 300
                    for label in labels) or
                type(position) is not int or not 0 <= position < len(rows)):
            raise ValueError('Invalid boundary playground history')
        history = [import_project(row) for row in rows]
        self.history, self.operations, self.position = history, labels, position
        self.revision += 1
        self.message = 'Reopened the checked boundary-twist exploration.'

    def state(self):
        project = self.project
        rows = []
        for factor in project.factors:
            try:
                svg = support_svg(factor, project.points)
                warning = ''
            except ValueError as error:
                svg, warning = '', str(error)
            splits = []
            if factor.power > 1:
                splits.append(('powers', f'Split into {factor.power} twists'))
            if not factor.half and factor.points == 2:
                splits.append(('halves', 'Split into half twists'))
            if not factor.half and factor.points == 3:
                splits.append(('lantern', 'Three pairwise twists'))
            rows.append(dict(asdict(factor), word=factor.word, label=factor.label,
                             svg=svg, warning=warning, height=row_height(factor),
                             splits=splits))
        return {
            'points': project.points,
            'power': project.power,
            'target_word': project.target_word,
            'factors': rows,
            'braid': braid_svg(project.factors, project.points),
            'export': project.to_dict(),
            'undo': self.position > 0,
            'redo': self.position < len(self.history)-1,
            'steps': list(self.operations),
            'position': self.position,
            'revision': self.revision,
            'message': self.message,
        }

    def _append(self, project, label):
        self.history = self.history[:self.position+1] + [project]
        self.operations = self.operations[:self.position+1] + [label]
        if len(self.history) > MAX_HISTORY:
            self.history.pop(0)
            self.operations.pop(0)
        self.position = len(self.history)-1

    def _example(self):
        """Record every checked step of the three-point half-twist exercise."""
        self._append(new_project(3, 1), 'Start three-point example')
        for label, operation in (
            ('Lantern: three pairwise twists', lambda p: p.split(0, 'lantern')),
            ('Split the first pair twist into halves', lambda p: p.split(0, 'halves')),
            ('Move the second half twist past the next factor', lambda p: p.move(1, 2)),
            ('Move the middle pair twist past the half twist', lambda p: p.move(1, 2)),
            ('Combine the final equal twists into a square', lambda p: p.combine(2)),
        ):
            self._append(operation(self.project), label)

    def mutate(self, payload):
        """Apply one exact operation atomically, leaving state intact on error."""
        if not isinstance(payload, dict) or payload.get('revision') != self.revision:
            raise ValueError('State changed; reload before editing')
        before = (self.history, self.operations, self.position, self.revision,
                  self.message)
        try:
            operation = payload.get('op')
            if operation == 'undo':
                if self.position == 0:
                    raise ValueError('Nothing to undo')
                self.position -= 1
                self.message = 'Undid the previous step.'
            elif operation == 'redo':
                if self.position == len(self.history)-1:
                    raise ValueError('Nothing to redo')
                self.position += 1
                self.message = 'Redid the next step.'
            elif operation == 'seek':
                position = payload.get('position')
                if type(position) is not int or not 0 <= position < len(self.history):
                    raise ValueError('Choose a saved history step')
                self.position = position
                self.message = f'Opened step {position+1}.'
            elif operation == 'new':
                project = new_project(payload.get('points'), payload.get('power'))
                self._append(project, f'Choose {project.points} points, power {project.power}')
                self.message = 'Started a new checked boundary-twist target.'
            elif operation == 'example':
                self._example()
                self.message = 'Loaded the checked three-point derivation; open its history to inspect each move.'
            elif operation == 'import':
                project = import_project(payload.get('document'))
                self._append(project, 'Import checked factorization')
                self.message = 'Imported a factorization with the exact target action verified.'
            elif operation in ('move', 'split', 'combine'):
                index = payload.get('index')
                if type(index) is not int:
                    raise ValueError('Choose a factor position')
                if operation == 'move':
                    target = payload.get('target')
                    project = self.project.move(index, target)
                    label = f'Hurwitz: factor {index+1} to {target+1}'
                elif operation == 'split':
                    kind = payload.get('kind')
                    project = self.project.split(index, kind)
                    label = f'Split factor {index+1} ({kind})'
                else:
                    project = self.project.combine(index)
                    label = f'Combine from factor {index+1}'
                self._append(project, label)
                self.message = 'The exact disk action still equals the chosen boundary twist.'
            else:
                raise ValueError('Unknown boundary playground operation')
            self.revision += 1
        except Exception:
            (self.history, self.operations, self.position, self.revision,
             self.message) = before
            raise

    def export_svg(self):
        return factorization_svg(self.project.factors, self.project.points)
