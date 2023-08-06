# VAI utils

## Quickstart

1. To use common Standardized code for develop use this package like below

`pip install vai-utils`

2. then add import statement like this

`from vai_utils import vai`
`from vai_utils import plot`

here is the code to use the plugin for converting html to json

    Data has to be in a string containing html tags.

        data = "<h1>Machine Learning </h1> <p>Machine learning is a field devoted to understanding and building methods that let machines learn – that is, methods that leverage data to improve computer performance on some set of tasks</p>"
        res = vai.html_to_json(data)


here is the code to use the plugin for converting json to html 

    Data has to be in a dictionary. 

        data = { "urls": { "id" :0 , "url" : "https://www.virtuousai.com/"  } }   
        res = vai.json_to_html(data)

here is the code to use the plugin for eprint with flush true 
        
        vai.eprint("data")

here is the code to use the plugin for getting html of given url

    vai.get_url_to_html(URL)

here is the code to use the plugin for getting json of given url

    vai.get_url_to_json(URL)

here is the code to use the plugin for storing html of given url

    vai.store_url_to_html(URL, input_dir)

here is the code to use the plugin for storing html of stored urls json file on given path

    vai.store_url_files_to_html(input_dir, output_dir)

here is the code to use the plugin for getting listing corrupted files

        vai.list_corrupted(PATH)

here is the code to use the plugin for getting listing duplicate files

        vai.list_duplicate(PATH)

here is the code to use the plugin for removing corrupted files

        files = vai.list_corrupted(PATH)   #Result return by list_corrupted 
        vai.remove_corrupted(files)

here is the code to use the crop images

        vai.crop_images(path,height, width) 

here is the code to use the college images

        vai.collage_images(path,height, width) 