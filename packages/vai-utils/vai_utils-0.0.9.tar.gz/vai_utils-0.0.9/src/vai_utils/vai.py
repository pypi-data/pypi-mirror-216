import requests
import json
import sys

python_base_url = "http://199.88.191.194:5007"
node_base_url = "http://199.88.191.194:5008"

def eprint(content):
    print(content, flush=True)
    return True

# def html_to_json(html):
#     request_url = base_url + "/html-to-json"
#     headers = {"Authorization": "25hD6Fpava"}
#     payload = json.dumps({ 
#         "html": html
#     })
#     response = requests.post(request_url, data=payload, headers=headers)
#     res = json.loads(response.text)
#     if ('message' in res):
#         return  sys.stderr.write(res['message'])
#     else :
#         return res

# def json_to_html(jsonData):
#     request_url = base_url + "/json-to-html"
#     headers = {"Authorization": "25hD6Fpava"}
#     payload = json.dumps({ 
#         "json": jsonData
#     })
#     response = requests.post(request_url, data=payload, headers=headers)
#     res = json.loads(response.text)
#     if ('message' in res):
#         return  sys.stderr.write(res['message'])
#     else :
#         return res
    
def get_url_to_html(url):
    request_url = node_base_url + "/convert?url="+url
    response = requests.get(request_url)
    res = json.loads(response.text)
    if ('message' in res):
        return  sys.stderr.write(res['message'])
    else :
        return res
    
def get_url_to_json(url):
    request_url = node_base_url + "/convert?url="+url+"&json=true"
    response = requests.get(request_url)
    res = json.loads(response.text)
    if ('message' in res):
        return  sys.stderr.write(res['message'])
    else :
        return res

def list_corrupted(path):
    request_url = python_base_url + "/list_corrupted?path="+path
    response = requests.get(request_url)
    res = json.loads(response.text)
    if ('message' in res):
        return  sys.stderr.write(res['message'])
    else :
        return res
    
def list_duplicate(path):
    request_url = python_base_url + "/list_duplicate?path="+path
    response = requests.get(request_url)
    res = json.loads(response.text)
    if ('message' in res):
        return  sys.stderr.write(res['message'])
    else :
        return res
    
def remove_corrupted(images):
    request_url = python_base_url + "/list_corrupted"
    payload =json.dumps({
        "images":images
    })
    response = requests.post(request_url,data=payload)
    res = json.loads(response.text)
    if ('message' in res):
        return  sys.stderr.write(res['message'])
    else :
        return res

def crop_images(path,height, width):
    request_url = node_base_url + "/crop?path="+path+'&width='+width+'&height='+height
    response = requests.get(request_url)
    res = json.loads(response.text)
    if ('message' in res):
        return  sys.stderr.write(res['message'])
    else :
        return res
    
def collage_images(path,height, width):
    request_url = python_base_url + "/collage_images?path="+path+'&width='+width+'&height='+height
    response = requests.get(request_url)
    res = json.loads(response.text)
    if ('message' in res):
        return  sys.stderr.write(res['message'])
    else :
        return res
    
def store_url_to_html(url,output):
    request_url = node_base_url + "/store-url-to-html?url="+url+'&output='+output
    response = requests.get(request_url)
    res = json.loads(response.text)
    if ('message' in res):
        return  sys.stderr.write(res['message'])
    else :
        return res
    
def store_url_files_to_html(input,output,chunk_size):
    request_url = python_base_url + "/store-url-files-to-html?file_path="+input+'&output='+output+'&chunk_size='+chunk_size 
    response = requests.get(request_url)
    res = json.loads(response.text)
    if ('message' in res):
        return  sys.stderr.write(res['message'])
    else :
        return res