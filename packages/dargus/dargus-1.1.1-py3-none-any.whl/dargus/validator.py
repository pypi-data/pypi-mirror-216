import re

from dargus.utils import get_item_from_json, dot2python, num_compare
from dargus.argus_exceptions import ValidationError


class Validator:
    def __init__(self, config, token=None):
        self._config = config
        self._rest_response = None
        self._rest_response_json = None
        self._current = None
        self._task = None
        self._stored_values = {}
        self._token = token

        self.validation = self.get_default_validation()
        if self._config.get('validation') is not None:
            self.validation.update(config.get('validation'))

    @staticmethod
    def get_default_validation():
        validation = {
            'timeDeviation': 100,
            'asyncRetryTime': 10,
            'ignore_time': False,
            'ignore_headers': [],
            'ignore_results': [],
            'fail_on_first': False
        }
        return validation

    def get_item(self, field):
        if field.startswith('<'):
            variable_name = field.split('.')[0].lstrip('<').rstrip('>')
            field = '.'.join(field.split('.')[1:])
            field_value = get_item_from_json(self._stored_values[variable_name], field)
        else:
            field_value = get_item_from_json(self._rest_response_json, field)
        return field_value

    def compare(self, field, value, operator='eq'):
        field_value = self.get_item(field)
        return num_compare(field_value, value, operator)

    def match(self, field, regex):
        field_value = self.get_item(field)
        return any(re.findall(regex, field_value))

    def empty(self, field):
        try:
            field_value = self.get_item(field)
        except (TypeError, KeyError, IndexError):
            return False
        return not field_value

    def list_length(self, field, value, operator='eq'):
        field_value = self.get_item(field)
        return num_compare(len(field_value), value, operator)

    def list_contains(self, field, value, expected=True):
        field_value = self.get_item(field)
        if expected:
            return value in field_value
        else:
            return value not in field_value

    @staticmethod
    def _to_python_lambda(value):
        value = value.replace('lambda', '')

        # From dot notation to python notation
        variables = filter(None, re.split('[-+*/=><|! ]', value))
        for v in variables:
            value = value.replace(v, dot2python(v))

        # Internal variables (e.g. "$QUERY_PARAMS")
        value = value.replace('$QUERY_PARAMS', 'self.task.query_params')

        value = 'lambda ' + value.replace('->', ':')
        return value

    def list_apply(self, field, value, all_=False):
        field_value = self.get_item(field)
        lambda_function = self._to_python_lambda(value)
        res = [eval(lambda_function, {'self': self})(i) for i in field_value]
        if all_:
            return all(res)
        else:
            return any(res)

    def list_equals(self, field, value, is_sorted=True):
        field_value = self.get_item(field)
        if len(field) != len(value):
            return False
        if is_sorted:
            return field_value == value
        else:
            return sorted(field_value) == sorted(value)

    def list_sorted(self, field, reverse=False):
        field_value = self.get_item(field)
        return field_value == sorted(field_value, reverse=reverse)

    def dict_equals(self, field, value):
        field_value = self.get_item(field)
        if len(field) != len(value):
            return False
        else:
            return field_value == value

    def store(self, field, variable_name):
        field_value = self.get_item(field)
        self._stored_values[variable_name] = field_value
        return True

    def _is_defined(self, method_name):
        return method_name in dir(self)

    def _validate_results(self, methods, exclude=None):
        results = []
        for method in methods:
            method_parts = re.search(r'^(.+?)\((.*)\)$', method)
            name = method_parts.group(1)
            args = method_parts.group(2)

            if name in exclude:
                continue

            if not self._is_defined(name):
                msg = 'Validation method "{}" not defined'
                raise AttributeError(msg.format(name))

            result = eval('self.{}({})'.format(name, args))

            # Raise error if fail_on_first is True
            if self.validation['fail_on_first'] and not result:
                msg = 'Validation function "{}" returned False'
                raise ValidationError(msg.format(method))

            results.append({'function': method, 'result': result})

        # Empty stored values
        self._stored_values = {}

        return results

    def validate_time(self, task_time):
        request_time = self._rest_response.elapsed.total_seconds()
        time_deviation = self.validation['timeDeviation']
        max_time = task_time + task_time*time_deviation/100
        min_time = task_time - task_time*time_deviation/100
        if not min_time < request_time < max_time:
            return False
        return True

    def validate_headers(self, task_headers, exclude=None):
        for key in task_headers.keys():
            if key not in exclude and (
                    key not in self._rest_response.headers.keys() or
                    self._rest_response.headers[key] != task_headers[key]
            ):
                return False
        return True

    def validate_status_code(self, task_status_code):
        if not task_status_code == self._rest_response.status_code:
            return False
        return True

    def validate(self, response, current):
        self._rest_response = response
        self._rest_response_json = response.json()
        self._current = current
        self._task = self._current.tests[0].tasks[0]
        results = []

        # Time
        if 'time' in self._task.validation and not self.validation['ignore_time']:
            results.append(
                {'function': 'validate_time',
                 'result': self.validate_time(self._task.validation['time'])}
            )

        # Headers
        if 'headers' in self._task.validation:
            result_headers = self.validate_headers(
                self._task.validation['headers'],
                exclude=self.validation['ignore_headers']
            )
            results.append({'function': 'validate_headers',
                            'result': result_headers})

        # Status code
        task_status_code = self._task.validation.get('status_code') \
            if 'status_code' in self._task.validation else 200
        results.append(
            {'function': 'validate_status_code',
             'result': self.validate_status_code(task_status_code)}
        )

        # Results
        if 'results' in self._task.validation:
            results += self._validate_results(
                self._task.validation['results'],
                exclude=self.validation['ignore_results']
            )

        return results

    def validate_async(self, async_jobs):
        pass
