'''
Created on Jun 12, 2012

@package: ally core http
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the content language header decoding.
'''

from ally.api.type import Locale
from ally.container.ioc import injected
from ally.core.http.spec.server import IDecoderHeader, IEncoderHeader
from ally.design.context import Context, requires, defines, optional
from ally.design.processor import HandlerProcessorProceed

# --------------------------------------------------------------------

class Request(Context):
    '''
    The request context.
    '''
    # ---------------------------------------------------------------- Required
    decoderHeader = requires(IDecoderHeader)
    # ---------------------------------------------------------------- Optional
    argumentsOfType = optional(dict)

class RequestContent(Context):
    '''
    The request content context.
    '''
    # ---------------------------------------------------------------- Defined
    language = defines(str, doc='''
    @rtype: string
    The language for the content.
    ''')

# --------------------------------------------------------------------

@injected
class ContentLanguageDecodeHandler(HandlerProcessorProceed):
    '''
    Implementation for a processor that provides the decoding of content language HTTP request header.
    '''

    nameContentLanguage = 'Content-Language'
    # The header name for the content language.

    def __init__(self):
        assert isinstance(self.nameContentLanguage, str), 'Invalid content language name %s' % self.nameContentLanguage
        super().__init__()

    def process(self, request:Request, requestCnt:RequestContent, **keyargs):
        '''
        @see: HandlerProcessorProceed.process
        
        Provides the content language decode for the request.
        '''
        assert isinstance(request, Request), 'Invalid request %s' % request
        assert isinstance(requestCnt, RequestContent), 'Invalid request content %s' % requestCnt
        assert isinstance(request.decoderHeader, IDecoderHeader), 'Invalid header decoder %s' % request.decoderHeader

        value = request.decoderHeader.retrieve(self.nameContentLanguage)
        if value:
            requestCnt.language = value
            if Request.argumentsOfType in request: request.argumentsOfType[Locale] = requestCnt.language

# --------------------------------------------------------------------

class Response(Context):
    '''
    The response context.
    '''
    # ---------------------------------------------------------------- Required
    encoderHeader = requires(IEncoderHeader)
    language = requires(str)

# --------------------------------------------------------------------

@injected
class ContentLanguageEncodeHandler(HandlerProcessorProceed):
    '''
    Implementation for a processor that provides the encoding of content language HTTP request header.
    '''

    nameContentLanguage = 'Content-Language'
    # The header name for the content language.

    def __init__(self):
        assert isinstance(self.nameContentLanguage, str), 'Invalid content language name %s' % self.nameContentLanguage
        super().__init__()

    def process(self, response:Response, **keyargs):
        '''
        @see: HandlerProcessorProceed.process
        
        Encodes the content language.
        '''
        assert isinstance(response, Response), 'Invalid response %s' % response
        assert isinstance(response.encoderHeader, IEncoderHeader), \
        'Invalid response header encoder %s' % response.encoderHeader

        if Response.language in response:
            response.encoderHeader.encode(self.nameContentLanguage, response.language)
