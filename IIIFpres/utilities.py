from . import  iiifpapi3 
import json

def modify_API3_json(path):
    """Modify an IIIF json file complaint with API 3.0
    This method parse only the frist level of the IIIF object. All the nested
    object are left as dict.

    It is faster compared to read read_API3_json.

    NOTE: the method assumes the IIIF object is complaint to API 3.0.

    Args:
        path (str): The path of the json file.
    """
    with open(path) as f: 
        t = json.load(f)
    t.pop('@context')
    entitydict = {'Manifest':iiifpapi3.Manifest(),
                  'Collection':iiifpapi3.Collection()}
    assert t['type'] in entitydict.keys(),"%s not a valid IIF object"%t['type']
    newobj = entitydict[t['type']]
    #TODO: find better solution .update will cause height and width to be set R.
    newobj.__dict__ = t
    return newobj 

def read_API3_json(path):
    """Read an IIIF json file complaint with API 3.0 and map the IIIF types to classes.

    This method parse the major IIIF types and map them to the iiifpapi3 classes.
    NOTE: the method assumes the IIIF object is complaint to API 3.0.

    Args:
        path (str): [description]
    """
    with open(path) as f: 
        t = json.load(f)    
    t.pop('@context')
   
    entitydict = {
     'Annotation':iiifpapi3.Annotation,
     'AnnotationPage':iiifpapi3.AnnotationPage,
     'Canvas':iiifpapi3.Canvas,
     'Collection':iiifpapi3.Collection,
     'FragmentSelector':iiifpapi3.FragmentSelector,
     'ImageApiSelector':iiifpapi3.ImageApiSelector,
     'Manifest':iiifpapi3.Manifest,
     'PointSelector':iiifpapi3.PointSelector,
     'Range':iiifpapi3.Range,
     'SpecificResource':iiifpapi3.SpecificResource,
     'Manifest':iiifpapi3.Manifest,
     'service':iiifpapi3.service,
     'thumbnail':iiifpapi3.thumbnail,
     'provider':iiifpapi3.provider,
     'homepage':iiifpapi3.homepage,
     'logo':iiifpapi3.logo,
     'rendering':iiifpapi3.rendering,
     'services':iiifpapi3.services,
     'start':iiifpapi3.start,
        }
    assert t['type'] in entitydict.keys(),"%s not a valid IIF object"%t['type']
    def map_to_class(obj):
        if 'items' in obj.keys():
            for n, item in enumerate(obj['items']):
                obj['items'][n] = map_to_class(item)   
        newobj = entitydict[obj['type']]()
        # TODO: find better solution .update will cause height and width to be set R.
        # newobj.__dict__ = newobj works apparently with no problem
        newobj.__dict__.update(obj)
        if obj['type'] == 'Canvas':
            if newobj.duration != None:
                newobj.set_duration(newobj.duration)
        return newobj
    newobj = map_to_class(t)
    return newobj 


def delete_object_byID(obj,id):
    if hasattr(obj,"__dict__"):
        obj = obj.__dict__
    if isinstance(obj,dict):
        for key,value in obj.items():
            if key == 'id' and value == id:
                return True
            delete_object_byID(value,id)
    if isinstance(obj,list):
        for item in obj:
            if delete_object_byID(item,id):
                obj.remove(item)
    else:
        pass

def remove_and_insert_new(obj,id,newobj):
    if hasattr(obj,"__dict__"):
        obj = obj.__dict__
    if isinstance(obj,dict):
        for key,value in obj.items():
            if key == 'id' and value == id:
                return True
            remove_and_insert_new(value,id)
    if isinstance(obj,list):
        for item in obj:
            if remove_and_insert_new(item,id):
                obj.remove(item)
                obj.append(newobj)
    else:
        pass

def check_valid_URI(URI):
    isvalid = True
    URI = URI.replace("https:/","",1)
    URI = URI.replace("http:/","",1)
    for indx, carat in enumerate(URI):
        if carat in r"""!"#$%&'()*+, :;<=>?@[\]^`{|}~ """:
            if carat == " ":
                carat = "a space"
            arrow = " "*(indx) + "^"
            isvalid = False
            print("I found: %s here. \n%s\n%s" %(carat,URI,arrow))
    return isvalid
                  