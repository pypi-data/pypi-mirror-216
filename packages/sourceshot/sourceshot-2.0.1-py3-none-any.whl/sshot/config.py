"""
Tools for token type and highlight config lookup.
"""
from pygments.token import *
from json import loads
class TokenChecker(object):
    """
    Token alias lookup.
    """
    def __init__(self):
        """
        All 30 token aliases.
        """
        self.config=[
            ('keyword',Keyword),
            ('builtin', Name.Builtin),
            ('decorator', Name.Decorator),
            ('class', Name.Class),
            ('func', Name.Function),
            ('exception',Name.Exception),
            ('identifier',Name),
            ('docstring',String.Doc),
            ('char',String.Char),
            ('escape',String.Escape),
            ('affix',String.Affix),
            ('regex',String.Regex),
            ('string',String),
            ('bin',Number.Bin),
            ('oct',Number.Oct),
            ('hex',Number.Hex),
            ('float',Number.Float),
            ('int',Number.Integer),
            ('date',Literal.Date),
            ('operator',Operator),
            ('punc',Punctuation),
            ('shebang',Comment.Hashbang),
            ('multiline-comment',Comment.Mutiline),
            ('preprocessor',Comment.Preproc),
            ('preprocessor-file',Comment.PreprocFile),
            ('comment',Comment.Single),
            ('whitespace',Whitespace),
            ('unknown',Text),
            ('error',Error),
            ('other',Other)
        ]
    def __call__(self,tok):
        for i,j in self.config:
            if is_token_subtype(tok,j):
                return i
    def __repr__(self):
        return '<TokenChecker>'
    def __str__(self):
        return self.__repr__()
    def get_all_names(self):
        return [i[0] for i in self.config]
class ColorConfig(object):
    """
    Syntax highlight config.
    """
    def __init__(self,cfdct,default=(0,0,0)):
        self._cf=cfdct
        self._d=default
    def __call__(self,tokname):
        if tokname in self._cf:
            return tuple(self._cf[tokname])
        return tuple(self._d)
    def __repr__(self):
        return '<ColorConfig {}, default is {}>'.format(self._cf,self._d)
    def __str__(self):
        return self.__repr__()
def color_config_from_json(json):
    """
    Get syntax highlight config from a JSON string
    for example:
    {
        "config":{
            "keyword":[127,0,0],
            "builtin":[0,0,127]
            }
    }
    :param json: A valid JSON string.
    :return: Syntax highlight config from the JSON string
    """
    dc=loads(json)
    if 'config' not in dc:
        raise ValueError("A color config JSON file should have a 'config' key")
    else:
        if 'default' in dc:
            return ColorConfig(dc['config'],default=dc['default'])
        else:
            return ColorConfig(dc['config'])