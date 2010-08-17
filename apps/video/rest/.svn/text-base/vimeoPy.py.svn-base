import md5
from xml.dom.minidom import parseString
from video.rest.restful_lib import Connection
from video.models import VimeoToken
from video.rest.MultipartPostHandler import MultipartPostHandler
import cookielib
import urllib2
import hashlib
import re

class VimeoClient:
    def __init__(self, api_key, secret):
        self.api_key = api_key
        self.secret = secret
        if(VimeoToken.objects.count()>0):
            self.token = VimeoToken.objects.all()[0].token
        else:
            self.token = False
        self.api_rest_url = "http://www.vimeo.com/api/rest/"
        self.api_auth_url = "http://www.vimeo.com/services/auth/"
        self.api_upload_url = "http://www.vimeo.com/services/upload/"

    def setToken(self, token):
        self.token = token

    def getToken(self):
        return self.token

    def generateAuthUrl(self):
        return self.generateUrl({"perms":"delete"}, self.api_auth_url)

    def generateSig(self, dic):
        s = ''
        params = dic.keys()
        params.sort()
        for param in params:
            s += str(param)+str(dic[param])
        return(md5.new(str(self.secret)+str(s)).hexdigest());

    def generateUrl(self, args, base=False):
        if(not base): base = self.api_rest_url
        s = '';
        args['api_key'] = self.api_key
        for arg in args:
            s += arg+"="+str(args[arg])+"&"

        return base+"?"+s+"api_sig="+self.generateSig(args);

    def hasAuth(self, perms):
        args = {'perms': perms}
        if(self.getToken()):
            rsp = self.call('vimeo.auth.checkToken')
            requested_perm_id = False
            actual_perm_id = False

            if(rsp.getElementsByTagName("auth")):
                available_perms = [None,'read', 'write', 'delete']
                requested_perm_id = available_perms.index(perms);
                if len(rsp.getElementsByTagName("perms")[0].childNodes)>0:
                    actual_perm_id = available_perms.index(rsp.getElementsByTagName("perms")[0].childNodes[0].nodeValue);
                else:
                    actual_perm_id = 0;

            #are we logged out or do wehave less permission than we asked for?
            if ((rsp.attributes['stat'].value == 'fail') or (requested_perm_id > actual_perm_id)):
                self.setToken(False)
                return False
            else:
                return True

        return False;

    def call(self, method, args={}):
        if(not args):args={}
        args['method'] = method;
        return self.request(args);


    def request(self, args):
        args['api_key'] = self.api_key;

        if(self.getToken()):
            args['auth_token'] = self.getToken()

        args['api_sig'] = self.generateSig(args)

        connection = Connection(self.api_rest_url)
        reply = connection.request_post("", args=args, headers={'Accept':'text/xml'})
        
        doc = parseString(reply['body'])
        return doc.documentElement

    def getUploadTicket(self):
        rsp = self.call('vimeo.videos.getUploadTicket');
        if(rsp.attributes['stat'].value == 'ok'):
            return rsp.getElementsByTagName("ticket")[0].attributes['id'].nodeValue
        else:
            raise Exception('Error Fetching Upload Ticket', 'Your upload limit was exceeded: '+rsp.toxml())

    def generateUploadSig(self, ticketId):
        args = {}
        args['api_key'] = self.api_key;
        args['auth_token'] = self.getToken()
        args['ticket_id'] = ticketId;
        return self.generateSig(args)

    def check_upload_status(self, ticket_id):
        args = {}
        args["ticket_id"] = ticket_id
        rsp = self.call('vimeo.videos.checkUploadStatus', args);
        if(rsp.attributes['stat'].value == 'ok'):
            return rsp.getElementsByTagName("ticket")[0].attributes['video_id'].nodeValue
        else:
            return False

    def upload(self, full_path_to_file):
        ticket = self.getUploadTicket();
        api_sig = self.generateUploadSig(ticket)
        post_data = {
            'api_key': self.api_key,
            'auth_token': self.getToken(),
            'ticket_id': ticket,
            'api_sig': api_sig,
            'video': open(full_path_to_file, 'rb'),
        }

        cookies = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies), MultipartPostHandler)
        response = opener.open(self.api_upload_url, post_data)
        reply = response.read()
        doc = parseString(reply)
        rsp = doc.documentElement
        if rsp.attributes['stat'].value == "ok":
            return ticket;
        else:
            return False;


