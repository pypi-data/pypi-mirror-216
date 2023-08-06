A capture moudle return base64 image with highlight

当你截图一个网页时，希望网页的部分内容可以高亮显示的同时截图，那么请继续往下看。

# Install

pip install Vulncapture

# Use

```
import Vulncapture
import base64
image=Vulncapture.run_snapshot(url='https://www.google.com',keyword='oo')
'''
run_snapshot() parmers
url : aim url
keyword : str
headers : dict
method : str('GET'/'POST')
if your aim url need to login , please set headers

auto set cookies
auto jump dialog and record dialog
auto stop jump to other domain
'''
print(image) # str
imgdata=base64.b64decode(image)
file=open('1.jpg','wb')
file.write(imgdata)
file.close()

imgdata2= Vulncapture.txt2image(data = 'it's password for me',keyword ='password')
print(imgdata2)
imgdata=base64.b64decode(imgdata2)
file=open('2.jpg','wb')
file.write(imgdata)
file.close()
```

