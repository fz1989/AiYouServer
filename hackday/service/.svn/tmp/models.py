from django.db import models
from datetime import datetime
# Create your models here.

class User(models.Model):
    userid = models.CharField(max_length=255)

class Gallery(models.Model):
    userid = models.CharField(max_length=255)
    galleryid = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    timestart = models.CharField(max_length=255)
    timeend = models.CharField(max_length=255)
    coverurl = models.CharField(max_length=255)
    description = models.TextField()

class Photo(models.Model):
    photoid = models.CharField(max_length=255)
    lat = models.CharField(max_length=255)
    lng = models.CharField(max_length=255)
    recordTime = models.CharField(max_length=255)
    description = models.TextField()
    place = models.CharField(max_length=255)
    userid = models.CharField(max_length=255)
    galleryid = models.CharField(max_length=255)

def add_user(userid, userpasskey):
    try:
        User(userid=userid, userpasskey=userpasskey).save()
        return True
    except:
        return False

def add_gallery(galleryid, location, timestart, timeend, coverurl, userid):
#    try:
        Gallery(galleryid=galleryid, location=location, timestart = timestart, timeend=timeend,
                coverurl=coverurl,userid=userid, description = "").save()
 #   except:
#        return False

def check_user(userid):
    ret = None
    ret = User.objects.filter(userid=userid)
    return ret

def check_gallery(galleryid):
    ret = None
    ret = Gallery.objects.filter(galleryid=galleryid)
    return ret

def add_photo(photoid, lat, lng, recordTime, description, place, userid, galleryid):
        if check_user(userid) and check_gallery(galleryid):
            Photo(photoid=photoid, lat=lat, lng=lng,
                    recordTime=recordTime,description=description,place=place,userid=userid,galleryid=galleryid).save()
            gallery = Gallery.objects.get(galleryid=galleryid)
            gallery.timeend = recordTime;
            gallery.save()

        if not check_user(userid):
            add_user(userid=userid, userpasskey='111')
        if not check_gallery(galleryid):
            add_gallery(galleryid, place ,str(datetime.now()),str(datetime.now()), photoid, userid=userid)
        Photo(photoid=photoid, lat=lat, lng=lng,
                recordTime=recordTime,description=description,place=place,userid=userid,galleryid=galleryid).save()

        return True

def get_photo(photoid):
    photo = Photo.objects.get(photoid=photoid)
    return  {'photoid':photo.photoid,
            'lat':photo.lat,
            'lng':photo.lng,
            'recordTime':photo.recordTime,
            'description':photo.description,
            'place':photo.place,
            'userid':photo.userid,
            'galleryid':photo.galleryid,
            }

def get_user(userid):
    try:
        user = User.objects.get(userid=userid)
        return {'userid':user.userid,
                'userpasskey':user.userpasskey,
                }
    except:
        return None

def get_gallery(galleryid):
    try:
        gallery = Gallery.objects.get(galleryid=galleryid)
        return {'galleryid':gallery.galleryid}
    except:
        return None

def get_all_user():
    return [user.userid for user in User.objects.all()]

def get_all_photo():
    return [photo.photoid for photo in Photo.objects.all()]

def get_all_gallery():
    return [gallery.galleryid for gallery in Gallery.objects.all()]

def get_photo_by_userid(userid):
    try:
        ret = []
        minTime = None
        maxTime = None
        for photo in Photo.objects.filter(userid=userid):
            ret.append(photo.photoid, photo.lat, photo.lng, photo.recordTime, photo.description,
                    photo.place, photoid.userid, photo.galleryid)
            if minTime == None or minTime > photo.recordTime:
                minTime = photo.recordTime
            if maxTime == None or maxTime < Photo.recordTime:
                maxTime = photo.recordTime
        return ret, minTime, maxTime;
    except:
        return None

def get_photo_by_galleryid(galleryid):
    ret = {'gallerydata':{},
            'photodata':[],
            }
    gallery = Gallery.objects.get(galleryid=galleryid)
    ret['gallerydata']['galleryid'] = gallery.galleryid
    ret['gallerydata']['userid'] = gallery.userid
    ret['gallerydata']['location'] = gallery.location
    ret['gallerydata']['timestart'] = gallery.timestart
    ret['gallerydata']['timeend'] = gallery.timeend
    ret['gallerydata']['description'] = gallery.description
    ret['gallerydata']['coverurl'] = gallery.coverurl

    i = 0
    for photo in Photo.objects.filter(galleryid=galleryid).all():
        print i
        print photo.photoid
        ret['photodata'].append(get_photo(photo.photoid))

    return ret

def get_gallery_by_userid(userid):
    ret = [];
    for gallery in Gallery.objects.filter(userid=userid).order_by("-timeend"):
        ret.append({'galleryid': gallery.galleryid,
            'location': gallery.location,
            'timestart': gallery.timestart,
            'timeend': gallery.timeend,
            'coverurl': gallery.coverurl})
    return ret

def update_gallery_description_byid(galleryid, description):
    gallery = Gallery.objects.get(galleryid=galleryid)
    gallery.description = description
    gallery.save()

def update_photo_description_byid(photoid, description):
    photo = Photo.objects.get(photoid=photoid)
    photo.description = description
    photo.save()


