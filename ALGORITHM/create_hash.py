import hashlib
import string
from urllib.parse import urlparse
import re


class HashUrl:
        
    ALPHABET = string.ascii_letters + string.digits


    @staticmethod
    def is_valid_url(url: str) -> bool:
        try:
            result = urlparse(url)
            
            if not all([result.scheme, result.netloc]):
                return False
                
            valid_schemes = {'http', 'https', 'ftp', 'ftps'}
            if result.scheme not in valid_schemes:
                return False
                
            domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z]{2,})+$'
            localhost_pattern = r'^localhost$|^127(\.[0-9]{1,3}){3}$|^\[::1\]$'
            
            if not (re.match(domain_pattern, result.netloc) or re.match(localhost_pattern, result.netloc)):
                return False
                
            return True
            
        except Exception:
            return False



    @staticmethod
    def to_base62(num, alphabet=ALPHABET):
        
        if num == 0:
            return alphabet[0]
        arr = []
        base = len(alphabet)
        while num:
            num, rem = divmod(num, base)
            arr.append(alphabet[rem])
        arr.reverse()
        return ''.join(arr)
    
    @staticmethod
    def short_hash_6_chars(url, length=6):

        if (HashUrl.is_valid_url(url) == False): return 0

        
        hash_object = hashlib.md5(url.encode())
        hash_bytes = hash_object.digest()
        
        num = int.from_bytes(hash_bytes[:4], byteorder='big')
        
        encoded = HashUrl.to_base62(num)
        
        return encoded[:length]
    
