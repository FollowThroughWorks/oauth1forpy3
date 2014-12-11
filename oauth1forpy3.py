import urllib.request
import time
import webbrowser

#WHAT IS REQUIRED:
    # First time around only: requestURL, accessURL, verificationURL; after acquiring access tokens, can replace with empty strings
    # Always: consumer key & secret, callback url, user agent
    # Access Tokens, necessary to retrieve page, either:
        # Use requestTokens, get user verification (userVerification is a kludgy solution), then accessTokensFromRequest
        # Use getAccessTokens, which is just the previously mentioned three combined
        # If you already have the access tokens, from prior verification, input them via assignAccessTokens
        
class Client:

    def __init__(self,consumerKey,consumerSecret,userAgent,callbackURL='',requestURL='',accessURL='',verificationURL=''):
        self.consumerKey = consumerKey
        self.consumerSecret = consumerSecret
        self.userAgent = userAgent
        self.requestURL = requestURL
        self.accessURL = accessURL
        self.verificationURL = verificationURL
        self.callbackURL = callbackURL
        self.user_verifier = ''
        self.request_tokens = {}
        self.access_token = ''
        self.access_token_secret = ''

    # Create headers for url request; tokens and secrets change depending on stage of authorization
    def headers(self,token,secret,verifier=""):
        contentType = "application/x-www-form-urlencoded"
        authorization = 'OAuth oauth_consumer_key="'+self.consumerKey+'",'\
                        'oauth_nonce="'+str(time.time()).split('.')[0]+'",'\
                        'oauth_token="'+token+'",'\
                        'oauth_signature="'+self.consumerSecret+'&'+secret+'",'\
                        'oauth_signature_method="PLAINTEXT",'\
                        'oauth_timestamp="'+str(time.time()).split('.')[0]+'",'\
                        'oauth_callback="'+self.callbackURL+'"'
        if(verifier!=""): authorization += ',oauth_verifier="'+verifier+'"'
        theseHeaders = {'Content-Type':contentType,'Authorization':authorization,'User-Agent':self.userAgent}
        return theseHeaders

    # Returns a dictionary with token and secret
    def get_tokens(self,url,token,secret,verifier=""):
        request = urllib.request.Request(url,headers=self.headers(token,secret,verifier))
        page = urllib.request.urlopen(request).read().decode('utf-8')

        new_token = page.split('&')[1].split('=')[1]
        new_secret = page.split('&')[0].split('=')[1]
        return {'token':new_token,'secret':new_secret}

    # Opens a browser and input to receive user verifier
    def user_verification(self,request_token):
        webbrowser.open(self.verificationURL + request_token)
        return input("Input verifier:  ")

    # Access Token and Secret are optional args; if not given, they are created; if given, they are set
    def set_access_token(self,input_token='',input_secret=''):
        if(input_token==''):
            request_tokens = self.get_tokens(self.requestURL,"","")
            verifier = self.user_verification(request_tokens['token'])
            access_tokens = self.get_tokens(self.accessURL,request_tokens['token'],request_tokens['secret'],verifier)
            self.access_token = access_tokens['token']
            self.access_token_secret = access_tokens['secret']
        else:
            self.access_token = input_token
            self.access_token_secret = input_secret

    # Use tokens to access web page
    def retrieve_page(self,url):
        request = urllib.request.Request(url,headers=self.headers(self.access_token,self.access_token_secret))
        page = urllib.request.urlopen(request).read().decode('utf-8')
        return page