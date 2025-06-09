import json


class CompactJSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder that formats simple lists on a single line.
    (Credits: Thank you AI for this encoder lol)
    
    Simple values (numbers, strings, booleans, None) in lists will be kept on one line.
    Complex values (objects, nested lists) will be formatted with proper indentation.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._indent = kwargs.get('indent', 2)
        self._current_indent = 0
    
    def encode(self, obj):
        if isinstance(obj, (list, tuple)):
            # For lists, check if all items are simple values (can be on one line)
            if all(isinstance(x, (int, float, str, bool)) or x is None for x in obj):
                return '[' + ', '.join(json.dumps(x, ensure_ascii=False) for x in obj) + ']'
            
            # For lists with complex items, handle with proper indentation
            self._current_indent += self._indent
            indent = ' ' * self._current_indent
            result = '['
            first = True
            
            for item in obj:
                if first:
                    first = False
                else:
                    result += ','
                result += '\n' + indent + self.encode(item)
            
            self._current_indent -= self._indent
            result += '\n' + ' ' * self._current_indent + ']'
            return result
            
        elif isinstance(obj, dict):
            # For dictionaries, always use newlines and proper indentation
            self._current_indent += self._indent
            indent = ' ' * self._current_indent
            result = '{\n' + indent
            first = True
            
            # Sort keys for consistent output
            for key in sorted(obj.keys(), key=str):
                if first:
                    first = False
                else:
                    result += ',\n' + indent
                # Ensure key is a string
                key_str = str(key) if not isinstance(key, str) else key
                result += json.dumps(key_str, ensure_ascii=False) + ': ' + self.encode(obj[key])
            
            self._current_indent -= self._indent
            result += '\n' + ' ' * self._current_indent + '}'
            return result
            
        else:
            # For simple values, use the default JSON encoding
            return json.dumps(obj, ensure_ascii=False)
