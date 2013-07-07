#! /usr/bin/env python
#coding=utf-8
from django.http import HttpResponse
from django.http import Http404
from hackday.service.models import *
from datetime import datetime
import json


def test_service(request):
    response = None
    if 'user_name' in request.REQUEST and 'tour_name' in request.REQUEST:
        user_name = request.REQUEST['user_name']
        tour_name = request.REQUEST['tour_name']
        print user_name, tour_name
        response = {'user_name':user_name, 'tour_name':tour_name}
        return HttpResponse(json.dumps(response))
    else:
        raise Http404()

def get_photo(request):
    response = None
    if 'galleryid' in request.REQUEST:
        galleryid = request.REQUEST['galleryid']
        response = get_photo_by_galleryid(galleryid)
        return HttpResponse(json.dumps(response))
    else:
        raise Http404()

def insert_photo(request):
    key_words = {'userid': '',
            'photoid':'',
            'lat': '',
            'lng': '',
            'description':'',
            'place':'',
            'galleryid':''}

    for key in key_words.keys():
        if key not in request.REQUEST:
            raise Http404()
        else:
            key_words[key] = request.REQUEST[key]


    key_words['recordTime'] = str(datetime.now())
    response = add_photo(key_words['photoid'],
                key_words['lat'],
                key_words['lng'],
                key_words['recordTime'],
                key_words['description'],
                key_words['place' ],
                key_words['userid'],
                key_words['galleryid'],
                )
    return HttpResponse(json.dumps({'response':response}))

def get_timeline(request):
    response = None
    if 'userid' in request.REQUEST:
        userid = request.REQUEST['userid']
        response = get_gallery_by_userid(userid)
        return HttpResponse(json.dumps({'data':response}))
    else:
        raise Http404()

def update_photo_description(request):
    if 'photoid' in request.REQUEST and 'description' in request.REQUEST:
        photoid = request.REQUEST['photoid']
        description = request.REQUEST['description']
        update_photo_description_byid(photoid, description)
        return HttpResponse(json.dumps({'response':'YES'}))

def update_gallery_description(request):
    if 'galleryid' in request.REQUEST and 'description' in request.REQUEST:
        galleryid = request.REQUEST['galleryid']
        description = request.REQUEST['description']
        update_gallery_description_byid(galleryid, description)
        return HttpResponse(json.dumps({'response':'YES'}))








