'''

"Data Collection and Processing with Python"
Final Project for Course 3 - OMDB and TasteDive Mashup

'''

import requests_with_caching
import json
import time

def get_movies_from_tastedive(mv_name):
    baseurl = "https://tastedive.com/api/similar"
    params_diction = {} 
    params_diction["q"] = mv_name
    params_diction["type"] = "movies"
    params_diction["limit"] = "5"
    resp =  requests_with_caching.get(baseurl, params=params_diction)
    movies = json.loads(resp.text)
    #print('resp:',movies)
    return movies 

def extract_movie_titles(mv_dct):
    lst =  []
    for d in mv_dct['Similar']['Results']:
        lst.append(d['Name'])
    #print('titles: ', lst)
    return lst[:5]

def get_related_titles(mvlst):
    rel_lst = []
    for title in mvlst:
        mvs = get_movies_from_tastedive(title)
        ttls = extract_movie_titles(mvs)
        for nam in ttls:
            if nam not in rel_lst: rel_lst.append(nam)
    #print('related titles:', rel_lst)
    return rel_lst


def get_movie_data(mv_name):
    baseurl = "http://www.omdbapi.com/"
    params_diction = {}
    params_diction["t"] = mv_name
    params_diction["r"] = "json" 
    resp = requests_with_caching.get(baseurl, params=params_diction)
    return json.loads(resp.text)

def get_movie_rating(movie_dict):
    #print('movi dict: ', movie_dict)
    rat = 0
    if len(movie_dict['Ratings']) > 1:
        if  movie_dict['Ratings'][1]['Source'] == 'Rotten Tomatoes':
            rat = int(movie_dict['Ratings'][1]['Value'][:2])
    #rint('rat:', rat)
    return rat

def get_sorted_recommendations(titles_list):
    #print('recom for: ', titles_list)
    rel_lst = get_related_titles(titles_list)
    #print('related titles: ', rel_lst)
    recomm_lst = []
    for t in rel_lst:
        mv = get_movie_data(t)
        rat = get_movie_rating(mv)
        recomm_lst.append((t, rat))
   
    recomm_lst = sorted(recomm_lst, key=lambda x: (x[1],x[0]), reverse=True)
    recomm_lst = [x[0] for x in recomm_lst]
    #print('recom list:', recomm_lst)
    return recomm_lst

#get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])
t1 = time.time()
#get_related_titles(["Bridesmaids", "Sherlock Holmes"])
#get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])
t2 = time.time()
print('time diff: ', t2 - t1)

