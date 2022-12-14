#!/usr/bin/env python
# coding: utf-8

# In[29]:


from owlready2 import * #Library for importing protege .owl file, including individuals and object properties

import networkx as nx #Graph Theory library, allows for making nodes, and edges. Can perform network analysis.
import matplotlib.pyplot as plt #Library that helps output graphs/plots or figures.
import numpy as np #Library that enables end user to work with arrays, esstentially a linear algebra library

from tabulate import tabulate #Library that can help make tables, to help organize output into user friendly output.


import itertools #Will help with iterating for PART 8


# In[31]:


onto = get_ontology('REDACTED') #Loading in .owl file, you can change the file as needed.
onto.load() #Loads in the .owl file
#This code does not have .owl provided due to privacy concerns. I cannot distribute the file.

# ## PART 1: Implement the SafeSim .owl file -- Owlready2 implementation

# We had just imported and loaded in the .owl file. Below we are now deriving what we need from the .owl file. This includes the weapons_type and sensor_type platforms. 
# 
# From each of these platforms, we are loading in the instances.

# In[32]:


#onto.safesim9_3 
namespace = onto.get_namespace("REDACTED")
namespace.Orwaca
namespace['REDACTED'].iri

#We are defining namespace here, what it is from the safesim9_3.owl as "Orwaca". This will enable us to search for
#anything in the .owl file.


# In[33]:


sensors = list(namespace.OW_Sensor_Type.instances()) 
#Creates a list of instances from the platform, OW_Sensor_Type platform. 

adj_sen = []
for i in sensors: 
    adj_sen.append(str(i)[11:]) 
#Modifying the original list of instances from OW_Sensor_Type, to delete the first 11 characters of each string.
    
print(adj_sen)


# In[34]:


weapons = list(namespace.OW_Weapon_Type.instances())
#Creates a list of instances from the platform, OW_Weapon_Type platform. 

adj_weapons = []
for i in weapons: 
    adj_weapons.append(str(i)[11:])
#Modifying the original list of instances from OW_Weapon_Type, to delete the first 11 characters of each string.

print(adj_weapons)


# In[35]:


communications = list(namespace.OW_Communications_Type.instances())
adj_com = []
for i in communications: 
    adj_com.append(str(i)[11:])
    
print(adj_com)


# ## PART 2: Find Object Properties for each instance.

# Now that we have the instances for the weapons and sensor type, it's time to find the object properities.
# 
# Below, for each instance, all of their object properities are found.

# In[36]:


dict_weapons = {} 

for i in adj_weapons:
    temp = onto.search_one(iri = '*' + str(i)).get_properties()
    temp_list = []
    for j in temp:
        temp_list.append(str(j)[11:])
    dict_weapons[i] = temp_list
#For each instance within adj_weapons, the object properities are derived from the .owl file.
#Each object property is then added to a dictionary, specifying each instance (the key), 
# to their object properties (the value).
    
print(dict_weapons)


# In[37]:


dict_sensors = {}

for i in adj_sen:
    temp = onto.search_one(iri = '*' + str(i)).get_properties()
    temp_list = []
    for j in temp:
        temp_list.append(str(j)[11:])
    dict_sensors[i] = temp_list

#For each instance within adj_weapons, the object properities are derived from the .owl file.
#Each object property is then added to a dictionary, specifying each instance (the key), 
# to their object properties (the value).

print(dict_sensors)


# In[24]:


dict_com = {}

for i in adj_com:
    temp = onto.search_one(iri = '*' + str(i)).get_properties()
    temp_list = []
    for j in temp:
        temp_list.append(str(j)[11:])
    dict_com[i] = temp_list

#For each instance within adj_com, the object properities are derived from the .owl file.
#Each object property is then added to a dictionary, specifying each instance (the key), 
# to their object properties (the value).

print(dict_com)


# ## THIS IS WHAT I AM WORKING ON

# In[119]:


SensorIsPartOfSystem_list = []
WeaponIsPartOfSystem_list = []

dict_weapons_Systems = {}
dict_sensors_Systems = {}

for i in dict_weapons:
    for j in dict_weapons[i]:
        if 'WeaponIsPartOfSystem' == j:
            WeaponIsPartOfSystem_list.append(i)
#print(WeaponIsPartOfSystem_list)

for i in WeaponIsPartOfSystem_list:
    temp_list = []
    temp = onto.search_one(iri = '*' + str(i)).WeaponIsPartOfSystem
    #print(temp)
    for j in temp:
        temp_list.append(str(j)[11:])
    dict_weapons_Systems[i] = temp_list
print(dict_weapons_Systems)


# In[118]:


dict_platforms_weapons = {}

for i in dict_weapons_Systems:
    temp_list = []
    #print(dict_weapons_Systems[i])
    #print(str(dict_weapons_Systems[i]).strip('[]'))
    if len(dict_weapons_Systems[i]) == 1:
        placeholder = str(dict_weapons_Systems[i]).strip('[]')
        placeholder = placeholder[1:]
        placeholder = placeholder[:-1]
        temp = onto.search_one(iri = '*' + placeholder).SystemIsAttachedToPlatform
        for j in temp:
            temp_list.append(str(j)[11:])
        
        dict_platforms_weapons[i] = temp_list
        
    else:
        for k in dict_weapons_Systems[i]:
            placeholder = k
            temp = onto.search_one(iri = '*' + placeholder).SystemIsAttachedToPlatform
            for j in temp:
                temp_list.append(str(j)[11:])
        
        dict_platforms_weapons[i] = temp_list    

print(dict_platforms_weapons)


# In[105]:





# In[ ]:





# ## PART 3: Filter out each platform (Weapons, Sensors, & Coms)

# Filters to only find instances that have the object properties that can Track, Target, Fix, Find, & Engage, to know the direction of the instances towards other instances (targets)

# In[120]:


AcanEngageO_weapons = []
AcanTargetO_weapons = []
AcanFixO_weapons = []
AcanFindO_weapons = []
AcanTrackO_weapons = []

AcanEngageO_weapons_names = []
AcanTargetO_weapons_names = []
AcanFixO_weapons_names = []
AcanFindO_weapons_names = []
AcanTrackO_weapons_names = []
#Empty lists that will be used for obtaining instances with a specific object property

for i in dict_weapons:
    for j in dict_weapons[i]:
        if 'AcanEngageO' == j:
            AcanEngageO_weapons_names.append(i+'_engage')
            AcanEngageO_weapons.append(i)
        if 'AcanTargetO' == j:
            AcanTargetO_weapons_names.append(i+'_target')
            AcanTargetO_weapons.append(i)
        if 'AcanFixO' == j:
            AcanFixO_weapons_names.append(i+'_fix')
            AcanFixO_weapons.append(i)
        if 'AcanFindO' == j:
            AcanFindO_weapons_names.append(i+'_find')
            AcanFindO_weapons.append(i)
        if 'AcanTrackO' == j:
            AcanTrackO_weapons_names.append(i+'_track')
            AcanTrackO_weapons.append(i)
#Iterates through weapon instances dictionary for engage, target, track, fix, or finding.
#Instances that do have those object properties are stored in their respective lists.
print(AcanEngageO_weapons)
print(AcanFindO_weapons)
print(AcanFixO_weapons)
print(AcanTargetO_weapons)
print(AcanTrackO_weapons)


# In[ ]:





# In[121]:


AcanEngageO_sensors = []
AcanTargetO_sensors = []
AcanFixO_sensors = []
AcanFindO_sensors = []
AcanTrackO_sensors = []

AcanEngageO_sensors_names = []
AcanTargetO_sensors_names = []
AcanFixO_sensors_names = []
AcanFindO_sensors_names = []
AcanTrackO_sensors_names = []

for i in dict_sensors:
    for j in dict_sensors[i]:
        if 'AcanEngageO' == j:
            AcanEngageO_sensors_names.append(i+'_engage')
            AcanEngageO_sensors.append(i)
        if 'AcanTargetO' == j:
            AcanTargetO_sensors_names.append(i+'_target')
            AcanTargetO_sensors.append(i)
        if 'AcanFixO' == j:
            AcanFixO_sensors_names.append(i+'_fix')
            AcanFixO_sensors.append(i)
        if 'AcanFindO' == j:
            AcanFindO_sensors_names.append(i+'_find')
            AcanFindO_sensors.append(i)
        if 'AcanTrackO' == j:
            AcanTrackO_sensors_names.append(i+'_track')
            AcanTrackO_sensors.append(i)
#Iterates through sensors instances dictionary for engage, target, track, fix, or finding.
#Instances that do have those object properties are stored in their respective lists.
print(AcanEngageO_sensors)
print(AcanFindO_sensors)
print(AcanFixO_sensors)
print(AcanTargetO_sensors)
print(AcanTrackO_sensors)


# In[122]:


CommIsActiveInNetwork_com = []


for i in dict_com:
    for j in dict_com[i]:
        if 'CommIsActiveInNetwork' == j:
            #AcanEngageO_sensors_names.append(i+'_engage')
            CommIsActiveInNetwork_com.append(i)
            
#Iterates through sensors instances dictionary for engage, target, track, fix, or finding.
#Instances that do have those object properties are stored in their respective lists.
print(CommIsActiveInNetwork_com)


# ## PART 4: Create a Dictionary that shows what instances can Track, Target, Fix, Find, or Engage, along with Coms Active Network

# Now that we know which instances can track, target, fix, find or engage...We are searching for the adversaries (the red team) that each instances (the blue team) can track, target, fix, find, and engage.

# In[123]:


dict_weapons_E = {}
dict_weapons_Find = {}
dict_weapons_Fix = {}
dict_weapons_T = {}
dict_weapons_Track = {}

print('Instances (key) will ENGAGE the following adversaries (value):')
#for every for loop, a search is being done for the adversaries that exhibit the desired object properties of instances.
for i in AcanEngageO_weapons:
    temp_list = []
    temp = onto.search_one(iri = '*' + str(i)).AcanEngageO
    
    for j in temp:
        temp_list.append(str(j)[11:])
    dict_weapons_E[i] = temp_list
print(dict_weapons_E)

print('\nInstances (key) will FIND the following adversaries (value):')

for i in AcanFindO_weapons:
    temp_list = []
    temp = onto.search_one(iri = '*' + str(i)).AcanFindO
    
    for j in temp:
        temp_list.append(str(j)[11:])
    dict_weapons_Find[i] = temp_list
print(dict_weapons_Find)

print('\nInstances (key) will FIX the following adversaries (value):')

for i in AcanFixO_weapons:
    temp_list = []
    temp = onto.search_one(iri = '*' + str(i)).AcanFixO
    
    for j in temp:
        temp_list.append(str(j)[11:])
    dict_weapons_Fix[i] = temp_list
print(dict_weapons_Fix)

print('\nInstances (key) will TARGET the following adversaries (value):')

for i in AcanTargetO_weapons:
    temp_list = []
    temp = onto.search_one(iri = '*' + str(i)).AcanTargetO
    
    for j in temp:
        temp_list.append(str(j)[11:])
    dict_weapons_T[i] = temp_list
print(dict_weapons_T)

print('\nInstances (key) will TRACK the following adversaries (value):')

for i in AcanTrackO_weapons:
    temp_list = []
    temp = onto.search_one(iri = '*' + str(i)).AcanTrackO
    
    for j in temp:
        temp_list.append(str(j)[11:])
    dict_weapons_Track[i] = temp_list
print(dict_weapons_Track)


# In[124]:


dict_sensors_E = {}
dict_sensors_Find = {}
dict_sensors_Fix = {}
dict_sensors_T = {}
dict_sensors_Track = {}
#for every for loop, a search is being done for the adversaries that exhibit the desired object properties of instances.
print('Instances (key) will ENGAGE the following adversaries (value):')

for i in AcanEngageO_sensors:
    temp_list = []
    temp = onto.search_one(iri = '*' + str(i)).AcanEngageO
    
    for j in temp:
        temp_list.append(str(j)[11:])
    dict_sensors_E[i] = temp_list
print(dict_sensors_E)

print('\nInstances (key) will FIND the following adversaries (value):')

for i in AcanFindO_sensors:
    temp_list = []
    temp = onto.search_one(iri = '*' + str(i)).AcanFindO
    
    for j in temp:
        temp_list.append(str(j)[11:])
    dict_sensors_Find[i] = temp_list
print(dict_sensors_Find)

print('\nInstances (key) will FIX the following adversaries (value):')

for i in AcanFixO_sensors:
    temp_list = []
    temp = onto.search_one(iri = '*' + str(i)).AcanFixO
    
    for j in temp:
        temp_list.append(str(j)[11:])
    dict_sensors_Fix[i] = temp_list
print(dict_sensors_Fix)

print('\nInstances (key) will TARGET the following adversaries (value):')

for i in AcanTargetO_sensors:
    temp_list = []
    temp = onto.search_one(iri = '*' + str(i)).AcanTargetO
    
    for j in temp:
        temp_list.append(str(j)[11:])
    dict_sensors_T[i] = temp_list
print(dict_sensors_T)

print('\nInstances (key) will TRACK the following adversaries (value):')

for i in AcanTrackO_sensors:
    temp_list = []
    temp = onto.search_one(iri = '*' + str(i)).AcanTrackO
    
    for j in temp:
        temp_list.append(str(j)[11:])
    dict_sensors_Track[i] = temp_list
print(dict_sensors_Track)


# In[125]:


dict_coms_ActiveNetwork = {}
#for every for loop, a search is being done for the active network that exhibit the desired object properties of instances.
print('Instances (key) is part of active network (value):')

for i in CommIsActiveInNetwork_com:
    temp_list = []
    temp = onto.search_one(iri = '*' + str(i)).CommIsActiveInNetwork
    
    for j in temp:
        temp_list.append(str(j)[11:])
    dict_coms_ActiveNetwork[i] = temp_list
print(dict_coms_ActiveNetwork)


# ## PART 5: Convert Platform (Weapons/Sensors/Coms) into Networks -- Networkx Implementation

# All data needed to make the graphs have now been loaded and synthesized into workable data. The workable data will now be manipulated once again to give a graphical representation in the form of nodes and edges.

# In[126]:


sensors_net_Fix = []
sensors_net_E = []
sensors_net_Find = []
sensors_net_T = []
sensors_net_Track = []

for i in dict_sensors_E:
    for j in dict_sensors_E[i]:
        temp_tuple = (i,j)
        sensors_net_E.append(temp_tuple)

#print(sensors_net_E)

for i in dict_sensors_Fix:
    for j in dict_sensors_Fix[i]:
        temp_tuple = (i,j)
        sensors_net_Fix.append(temp_tuple)

#print(sensors_net_Fix)

for i in dict_sensors_Find:
    for j in dict_sensors_Find[i]:
        temp_tuple = (i,j)
        sensors_net_Find.append(temp_tuple)

#print(sensors_net_Find)

for i in dict_sensors_T:
    for j in dict_sensors_T[i]:
        temp_tuple = (i,j)
        sensors_net_T.append(temp_tuple)

#print(sensors_net_T)

for i in dict_sensors_Track:
    for j in dict_sensors_Track[i]:
        temp_tuple = (i,j)
        sensors_net_Track.append(temp_tuple)

#print(sensors_net_Track)


# In[127]:


weapons_net_Fix = []
weapons_net_E = []
weapons_net_Find = []
weapons_net_T = []
weapons_net_Track = []

for i in dict_weapons_E:
    for j in dict_weapons_E[i]:
        temp_tuple = (i,j)
        weapons_net_E.append(temp_tuple)

#print(weapons_net_E)

for i in dict_weapons_Fix:
    for j in dict_weapons_Fix[i]:
        temp_tuple = (i,j)
        weapons_net_Fix.append(temp_tuple)

#print(weapons_net_Fix)

for i in dict_weapons_Find:
    for j in dict_weapons_Find[i]:
        temp_tuple = (i,j)
        weapons_net_Find.append(temp_tuple)

#print(weapons_net_Find)

for i in dict_weapons_T:
    for j in dict_weapons_T[i]:
        temp_tuple = (i,j)
        weapons_net_T.append(temp_tuple)

#print(weapons_net_T)

for i in dict_weapons_Track:
    for j in dict_weapons_Track[i]:
        temp_tuple = (i,j)
        weapons_net_Track.append(temp_tuple)

#print(weapons_net_Track)


# In[128]:


com_net_ActiveN = []
dict_coms_ActiveNetwork

for i in dict_coms_ActiveNetwork:
    for j in dict_coms_ActiveNetwork[i]:
        temp_tuple = (i,j)
        com_net_ActiveN.append(temp_tuple)

#print(com_net_ActiveN)


# The two terminals above are making the node tuples of the graph that displays the weapons or sensors that can hit the targets

# In[129]:


sensors_net_Fix_name = []
sensors_net_E_name = []
sensors_net_Find_name = []
sensors_net_T_name = []
sensors_net_Track_name = []

for i in dict_sensors_E:
    for j in dict_sensors_E[i]:
        temp_tuple = (i+'_engage',j)
        sensors_net_E_name.append(temp_tuple)

#print(sensors_net_E)

for i in dict_sensors_Fix:
    for j in dict_sensors_Fix[i]:
        temp_tuple = (i+'_fix',j)
        sensors_net_Fix_name.append(temp_tuple)

#print(sensors_net_Fix)

for i in dict_sensors_Find:
    for j in dict_sensors_Find[i]:
        temp_tuple = (i+'_find',j)
        sensors_net_Find_name.append(temp_tuple)

#print(sensors_net_Find)

for i in dict_sensors_T:
    for j in dict_sensors_T[i]:
        temp_tuple = (i+'_target',j)
        sensors_net_T_name.append(temp_tuple)

#print(sensors_net_T)

for i in dict_sensors_Track:
    for j in dict_sensors_Track[i]:
        temp_tuple = (i+'_track',j)
        sensors_net_Track_name.append(temp_tuple)

#print(sensors_net_T)


# In[130]:


weapons_net_Fix_name = []
weapons_net_E_name = []
weapons_net_Find_name = []
weapons_net_T_name = []
weapons_net_Track_name = []

for i in dict_weapons_E:
    for j in dict_weapons_E[i]:
        temp_tuple = (i+'_engage',j)
        weapons_net_E_name.append(temp_tuple)

#print(weapons_net_E)

for i in dict_weapons_Fix:
    for j in dict_weapons_Fix[i]:
        temp_tuple = (i+'_fix',j)
        weapons_net_Fix_name.append(temp_tuple)

#print(weapons_net_Fix)

for i in dict_weapons_Find:
    for j in dict_weapons_Find[i]:
        temp_tuple = (i+'_find',j)
        weapons_net_Find_name.append(temp_tuple)

#print(weapons_net_Find)

for i in dict_weapons_T:
    for j in dict_weapons_T[i]:
        temp_tuple = (i+'_target',j)
        weapons_net_T_name.append(temp_tuple)

#print(weapons_net_T)

for i in dict_weapons_Track:
    for j in dict_weapons_Track[i]:
        temp_tuple = (i+'_track',j)
        weapons_net_Track_name.append(temp_tuple)

#print(weapons_net_Track)


# In[ ]:





# The two terminals above are making the node tuples for the graph that can show which parts of the sensors or weapons that can target, fix, track, find, or engage the adversaries

# In[131]:


G = nx.DiGraph() #Specifying a directed graph, this is for the weapons or sensors acting on the adversaries
G_null = nx.DiGraph() #Directed graph, specifying the object properties acting on adversaries


# In[132]:



G.add_edges_from(sensors_net_T)
G.add_edges_from(sensors_net_E)
G.add_edges_from(sensors_net_Fix)
G.add_edges_from(sensors_net_Find)
G.add_edges_from(sensors_net_Track)

G.add_edges_from(weapons_net_T)
G.add_edges_from(weapons_net_E)
G.add_edges_from(weapons_net_Fix)
G.add_edges_from(weapons_net_Find)
G.add_edges_from(weapons_net_Track)

G.add_edges_from(com_net_ActiveN)

G_null.add_edges_from(sensors_net_T_name)
G_null.add_edges_from(sensors_net_E_name)
G_null.add_edges_from(sensors_net_Fix_name)
G_null.add_edges_from(sensors_net_Find_name)
G_null.add_edges_from(sensors_net_Track_name)

G_null.add_edges_from(weapons_net_T_name)
G_null.add_edges_from(weapons_net_E_name)
G_null.add_edges_from(weapons_net_Fix_name)
G_null.add_edges_from(weapons_net_Find_name)
G_null.add_edges_from(weapons_net_Track_name)

G_null.add_edges_from(com_net_ActiveN)

super_net_list = [sensors_net_T,sensors_net_E,sensors_net_Fix,sensors_net_Find,sensors_net_Track,
                  weapons_net_T,weapons_net_E,weapons_net_Fix,weapons_net_Find,weapons_net_Track,
                  com_net_ActiveN]

super_net_list_name = [sensors_net_T_name,sensors_net_E_name,sensors_net_Fix_name,sensors_net_Find_name,
                       sensors_net_Track_name,
                       weapons_net_T_name,weapons_net_E_name,weapons_net_Fix_name,weapons_net_Find_name,
                       weapons_net_Track_name,
                       com_net_ActiveN]


# In[133]:


comms_links_nodes = []
for i in dict_coms_ActiveNetwork:
    for j in dict_coms_ActiveNetwork[i]:
        if j not in comms_links_nodes:
            comms_links_nodes.append(j)
        
print(comms_links_nodes)


# In[134]:


weapon_engage_nodes_names = []
weapon_target_nodes_names = []
weapon_track_nodes_names = []
weapon_fix_nodes_names = []
weapon_find_nodes_names = []

sensor_engage_nodes_names = []
sensor_target_nodes_names = []
sensor_track_nodes_names = []
sensor_fix_nodes_names = []
sensor_find_nodes_names = []

for i in AcanEngageO_weapons_names:
    weapon_engage_nodes_names.append(i)
for i in AcanFindO_weapons_names:
    weapon_find_nodes_names.append(i)
for i in AcanFixO_weapons_names:
    weapon_fix_nodes_names.append(i)
for i in AcanTargetO_weapons_names:
    weapon_target_nodes_names.append(i)
for i in AcanTrackO_weapons_names:
    weapon_track_nodes_names.append(i)

for i in AcanEngageO_sensors_names:
    sensor_engage_nodes_names.append(i)
for i in AcanFindO_sensors_names:
    sensor_find_nodes_names.append(i)
for i in AcanFixO_sensors_names:
    sensor_fix_nodes_names.append(i)
for i in AcanTargetO_sensors_names:
    sensor_target_nodes_names.append(i)
for i in AcanTrackO_sensors_names:
    sensor_track_nodes_names.append(i)

#This is a color map, giving nodes color on the basis on object property.
#More specifically, if they can find, fix, track, target, and engage.
color_map_null = []
for node in G_null:
    if node in weapon_engage_nodes_names :
        color_map_null.append('blue')
    elif node in sensor_engage_nodes_names :
        color_map_null.append('blue')
    
    elif node in weapon_target_nodes_names :
        color_map_null.append('purple')
    elif node in sensor_target_nodes_names :
        color_map_null.append('purple')
    
    elif node in weapon_track_nodes_names :
        color_map_null.append('olive')
    elif node in sensor_track_nodes_names :
        color_map_null.append('olive')
        
    elif node in weapon_fix_nodes_names :
        color_map_null.append('green')
    elif node in sensor_fix_nodes_names :
        color_map_null.append('green')
        
    elif node in weapon_find_nodes_names :
        color_map_null.append('orange')
    elif node in sensor_find_nodes_names :
        color_map_null.append('orange')
    
    elif node in CommIsActiveInNetwork_com:
        color_map_null.append('aqua')
    elif node in comms_links_nodes:
        color_map_null.append('#76EEC6')

    
    else: 
        color_map_null.append('red')

edge_colors = 'black'


# In[135]:


weapon_engage_nodes = []
weapon_target_nodes = []
weapon_fix_nodes = []
weapon_find_nodes = []

sensor_engage_nodes = []
sensor_target_nodes = []
sensor_fix_nodes = []
sensor_find_nodes = []

for i in AcanEngageO_weapons:
    weapon_engage_nodes.append(i)
for i in AcanFindO_weapons:
    weapon_find_nodes.append(i)
for i in AcanFixO_weapons:
    weapon_fix_nodes.append(i)
for i in AcanTargetO_weapons:
    weapon_target_nodes.append(i)

for i in AcanEngageO_sensors:
    sensor_engage_nodes.append(i)
for i in AcanFindO_sensors:
    sensor_find_nodes.append(i)
for i in AcanFixO_sensors:
    sensor_fix_nodes.append(i)
for i in AcanTargetO_sensors:
    sensor_target_nodes.append(i)

#This is a color map, giving nodes color on the basis of if the node is a weapon,sensor, or com node.
color_map = []
for node in G:
    if node in weapon_engage_nodes :
        color_map.append('blue')
    elif node in sensor_engage_nodes :
        color_map.append('purple')
    
    elif node in weapon_target_nodes :
        color_map.append('blue')
    elif node in sensor_target_nodes :
        color_map.append('purple')
        
    elif node in weapon_fix_nodes :
        color_map.append('blue')
    elif node in sensor_fix_nodes :
        color_map.append('purple')
        
    elif node in weapon_find_nodes :
        color_map.append('blue')
    elif node in sensor_find_nodes :
        color_map.append('purple')
        
    elif node in CommIsActiveInNetwork_com:
        color_map.append('aqua')
    elif node in comms_links_nodes:
        color_map.append('#76EEC6')
        
    else: 
        color_map.append('red')


# In[136]:


#Positioning of nodes within G graph.
#pos = nx.spring_layout(G)
pos_G = nx.nx_pydot.graphviz_layout(G)
#pos = nx.circular_layout(G)
#pos = nx.random_layout(G)


# In[137]:


#Positioning of nodes within G_null graph. Uncomment and comment the positions that work best visually.
#pos = nx.spring_layout(G)
pos = nx.nx_pydot.graphviz_layout(G_null)
#pos = nx.circular_layout(G_null)
#pos = nx.random_layout(G_null)


# ## PART 6: Displaying the graphs

# Now that graphs are prepared. They can be displayed!

# Below is a graph that specifies which tasks associated with each weapon or sensor is acting. Aka, the find, fix, track, target, engage.
# 
# 
# Orange = Find;
# 
# Green = Fix;
# 
# Olive = Track;
# 
# Purple = Target;
# 
# Blue = Engage;
# 
# Red = Adversary;
# 
# Aqua = Communication;
# 
# Aquamarine = Datalink 

# In[138]:


plt.figure(1,figsize=(100,75))

nx.draw_networkx_nodes(G_null,pos, node_color=color_map_null,node_size=6000)

for i in super_net_list_name:
    nx.draw_networkx_edges(G_null,pos, edgelist = i, edge_color=edge_colors,arrowsize=30)
nx.draw_networkx_labels(G_null,pos,font_color = "black", font_size = 80, font_family = "Times New Roman")

plt.show()


# Below is a graph that shows the sensors or weapons that are acting, as well as the adversaries only.
# 
# Purple = Sensor
# 
# Blue = Weapon
# 
# Red = Adversary
# 
# Aqua = Communication
# 
# Aquamarine = Datalink

# In[139]:


plt.figure(1,figsize=(50,50))

nx.draw_networkx_nodes(G,pos_G, node_color=color_map,node_size=5000)

for i in super_net_list:
    nx.draw_networkx_edges(G,pos_G, edgelist = i, edge_color=edge_colors,arrowsize=30)
nx.draw_networkx_labels(G,pos_G,font_color = "black", font_size = 50, font_family = "Times New Roman")

plt.show()


# ## PART 7: Manipulating data to find different variations of Find -> Fix -> Track -> Target -> Engage for every adversary

# Now that we have all the data, and represented on the graph. We can now start to manipulate the data to eventually show the different kill chains that can engage a specific target the end user desires.

# In[140]:


#In this terminal, we are creating dictionaries with adversaries and their respective weapons and sensors. 
#Eventually, both the sensors and weapons will converge into one dictionary for each object type.
adversaries = []
dict_adv_Engage_ref = {}
dict_adv_Find_ref = {}
dict_adv_Fix_ref = {}
dict_adv_Target_ref = {}
dict_adv_Track_ref = {}

for i in dict_weapons_E:
    for j in dict_weapons_E[i]:
        if j not in adversaries:
            adversaries.append(j)
        dict_adv_Engage_ref[j] = i

for i in dict_weapons_Find:
    for j in dict_weapons_Find[i]:
        if j not in adversaries:
            adversaries.append(j)
        dict_adv_Find_ref[j] = i
        
for i in dict_weapons_Fix:
    for j in dict_weapons_Fix[i]:
        if j not in adversaries:
            adversaries.append(j)
        dict_adv_Fix_ref[j] = i
            
for i in dict_weapons_T:
    for j in dict_weapons_T[i]:
        if j not in adversaries:
            adversaries.append(j)
        dict_adv_Target_ref[j] = i
            
for i in dict_weapons_Track:
    for j in dict_weapons_Track[i]:
        if j not in adversaries:
            adversaries.append(j)
        dict_adv_Track_ref[j] = i
        
for i in dict_sensors_E:
    for j in dict_sensors_E[i]:
        if j not in adversaries:
            adversaries.append(j)
        dict_adv_Engage_ref[j] = i
            
for i in dict_sensors_Find:
    for j in dict_sensors_Find[i]:
        if j not in adversaries:
            adversaries.append(j)
        dict_adv_Find_ref[j] = i
            
for i in dict_sensors_Fix:
    for j in dict_sensors_Fix[i]:
        if j not in adversaries:
            adversaries.append(j)
        dict_adv_Fix_ref[j] = i
            
for i in dict_sensors_T:
    for j in dict_sensors_T[i]:
        if j not in adversaries:
            adversaries.append(j)
        dict_adv_Target_ref[j] = i
            
for i in dict_sensors_Track:
    for j in dict_sensors_Track[i]:
        if j not in adversaries:
            adversaries.append(j)
        dict_adv_Track_ref[j] = i
            
#print(adversaries)
#print("\nAdversaries (Key) that can be FIND by instance")
#print(dict_adv_Find_ref)
#print("\nAdversaries (Key) that can be FIX by instance")
#print(dict_adv_Fix_ref)
#print("\nAdversaries (Key) that can be TRACK by instance")
#print(dict_adv_Track_ref)
#print("\nAdversaries (Key) that can be TARGET by instance")
#print(dict_adv_Target_ref)
#print("\nAdversaries (Key) that can be ENGAGE by instance")
#print(dict_adv_Engage_ref)


# FIND = FID, FIX = FIX, TRACK = TRK, TARGET = TGT, ENGAGE = ENG

# In[141]:


#In this terminal, same as above is going on, but with specifications on if the instances are fixing, finding, etc.
dict_adv_Engage_specified = {}
dict_adv_Find_specified = {}
dict_adv_Fix_specified = {}
dict_adv_Target_specified = {}
dict_adv_Track_specified = {}

for i in dict_weapons_E:
    for j in dict_weapons_E[i]:
        try:
            temp_list = dict_adv_Engage_specified[j]
        except KeyError:
            temp_list = []
        i_temp = i+'_ENG'
        if i_temp not in temp_list:
            temp_list.append(i_temp)
        dict_adv_Engage_specified[j] = temp_list

for i in dict_weapons_T:
    for j in dict_weapons_T[i]:
        try:
            temp_list = dict_adv_Target_specified[j]
        except KeyError:
            temp_list = []
        i_temp = i+'_TGT'
        if i not in temp_list:
            temp_list.append(i_temp)
        dict_adv_Target_specified[j] = temp_list

for i in dict_weapons_Find:
    for j in dict_weapons_Find[i]:
        try:
            temp_list = dict_adv_Find_specified[j]
        except KeyError:
            temp_list = []
        i_temp = i+'_FID'
        if i_temp not in temp_list:
            temp_list.append(i_temp)
        dict_adv_Find_specified[j] = temp_list

for i in dict_weapons_Fix:
    for j in dict_weapons_Fix[i]:
        try:
            temp_list = dict_adv_Fix_specified[j]
        except KeyError:
            temp_list = []
        i_temp = i+'_FIX'
        if i_temp not in temp_list:
            temp_list.append(i_temp)
        dict_adv_Fix_specified[j] = temp_list
        
for i in dict_weapons_Track:
    for j in dict_weapons_Track[i]:
        try:
            temp_list = dict_adv_Track_specified[j]
        except KeyError:
            temp_list = []
        i_temp = i+'_TRK'
        if i_temp not in temp_list:
            temp_list.append(i_temp)
        dict_adv_Track_specified[j] = temp_list


# In[142]:


for i in dict_sensors_E:
    for j in dict_sensors_E[i]:
        try:
            temp_list = dict_adv_Engage_specified[j]
        except KeyError:
            temp_list = []
        i_temp = i+'_ENG'
        if i_temp not in temp_list:
            temp_list.append(i_temp)
        dict_adv_Engage_specified[j] = temp_list

for i in dict_sensors_T:
    for j in dict_sensors_T[i]:
        try:
            temp_list = dict_adv_Target_specified[j]
        except KeyError:
            temp_list = []
        i_temp = i+'_TGT'
        if i_temp not in temp_list:
            temp_list.append(i_temp)
        dict_adv_Target_specified[j] = temp_list

for i in dict_sensors_Find:
    for j in dict_sensors_Find[i]:
        try:
            temp_list = dict_adv_Find_specified[j]
        except KeyError:
            temp_list = []
        i_temp = i+'_FID'
        if i_temp not in temp_list:
            temp_list.append(i_temp)
        dict_adv_Find_specified[j] = temp_list

for i in dict_sensors_Fix:
    for j in dict_sensors_Fix[i]:
        try:
            temp_list = dict_adv_Fix_specified[j]
        except KeyError:
            temp_list = []
        i_temp = i+'_FIX'
        if i_temp not in temp_list:
            temp_list.append(i_temp)
        dict_adv_Fix_specified[j] = temp_list
        
for i in dict_sensors_Track:
    for j in dict_sensors_Track[i]:
        try:
            temp_list = dict_adv_Track_specified[j]
        except KeyError:
            temp_list = []
        i_temp = i+'_TRK'
        if i_temp not in temp_list:
            temp_list.append(i_temp)
        dict_adv_Track_specified[j] = temp_list

print(dict_adv_Track_specified)
print('\n',dict_adv_Engage_specified)
print('\n',dict_adv_Target_specified)
print('\n',dict_adv_Fix_specified)
print('\n',dict_adv_Find_specified)


# ## PART 8: Finding the all possible combinations of kill chains, and exporting it into a HTML (Web) based table.

# Given the adversary of interest, now we are able to map out what kill chains are possible.

# In[156]:


Adversary_of_interest = 'REDACTED'



#terminology aligned, 


# In[157]:


Find = dict_adv_Find_specified[Adversary_of_interest]
Fix = dict_adv_Fix_specified[Adversary_of_interest]
Track = dict_adv_Track_specified[Adversary_of_interest]
Target = dict_adv_Target_specified[Adversary_of_interest]
Engage = dict_adv_Engage_specified[Adversary_of_interest]
Adversary_of_interest_list = [Adversary_of_interest]



# In[158]:


all_combinations = list(itertools.product(Find, Fix, Track, Target, Engage, Adversary_of_interest_list))


# In[159]:


Kill_chains = [];
for i in all_combinations:
    temp_list = []
    for j in i:
        temp_list.append(j[:-4])
    Kill_chains.append(temp_list)
#print(Kill_chains)


# In[160]:


all_combinations_no_repeats = list(itertools.product(Find, Fix, Track, Target, Engage, Adversary_of_interest_list))

Kill_chains_no_repeats = []
for i in all_combinations:
    temp_list = []
    for j in i:
        temp_list.append(j[:-4])
    Kill_chains_no_repeats.append(temp_list)

index_counter = 0
no_repeats_new_list = []
for i in Kill_chains_no_repeats:
    # create a set from the list
    #print(i)
    myset = set(i)
    if len(i) != len(myset):
        #print("duplicates found in the list")
        Kill_chains_no_repeats.pop(index_counter)
    else:
        #print("No duplicates found in the list")
        no_repeats_new_list.append(i)
    index_counter = index_counter + 1

print(no_repeats_new_list)


# In[161]:


combo_list = [['ID','Finding','Fixing','Tracking','Targeting','Engaging','Adversary']]
counter = 1
for i in Kill_chains:
    temp_list = []
    temp_node_name = str(counter)
    temp_list.append(temp_node_name)
    temp_node_name = i[0]
    temp_list.append(temp_node_name)
    temp_node_name = i[1]
    temp_list.append(temp_node_name)
    temp_node_name = i[2]
    temp_list.append(temp_node_name)
    temp_node_name = i[3]
    temp_list.append(temp_node_name)
    temp_node_name = i[4]
    temp_list.append(temp_node_name)
    temp_node_name = i[5]
    temp_list.append(temp_node_name)
    combo_list.append(temp_list)
    counter = counter + 1

html_conversion_kill_chains = tabulate(combo_list,headers='firstrow', tablefmt='html')
print(html_conversion_kill_chains)


# In[162]:


combo_list_no_repeats = [['ID','Finding','Fixing','Tracking','Targeting','Engaging','Adversary']]
counter = 1
for i in no_repeats_new_list:
    temp_list = []
    temp_node_name = str(counter)
    temp_list.append(temp_node_name)
    temp_node_name = i[0]
    temp_list.append(temp_node_name)
    temp_node_name = i[1]
    temp_list.append(temp_node_name)
    temp_node_name = i[2]
    temp_list.append(temp_node_name)
    temp_node_name = i[3]
    temp_list.append(temp_node_name)
    temp_node_name = i[4]
    temp_list.append(temp_node_name)
    temp_node_name = i[5]
    temp_list.append(temp_node_name)
    combo_list_no_repeats.append(temp_list)
    counter = counter + 1

html_conversion_kill_chains_no_repeats = tabulate(combo_list_no_repeats,headers='firstrow', tablefmt='html')
print(html_conversion_kill_chains_no_repeats)


# ## PART 9: Centrality Calculations 

# Calculating different centrality types, with hopes of using this information to next find the optimal kill chain for success, given the different kill chains and information needed.

# In[150]:


Adjacent_matrix_G_null = nx.to_numpy_matrix(G_null)
print(Adjacent_matrix_G_null)


# In[151]:


eigen_centrality = nx.eigenvector_centrality(G_null,max_iter=200)
sorted_ec = sorted(eigen_centrality)

eigen_c_list = [['Node Name','Eigenvector Centrality']]
for i in sorted_ec:
    temp_list = []
    temp_node_name = i
    temp_list.append(temp_node_name)
    
    temp_node_ec = eigen_centrality[temp_node_name]
    temp_list.append(temp_node_ec)
    eigen_c_list.append(temp_list)
    
print(tabulate(eigen_c_list,headers='firstrow', tablefmt='fancy_grid'))


# In[152]:


eigen_centrality = nx.eigenvector_centrality(G_null,max_iter=200)
sorted_ec = sorted(eigen_centrality)

eigen_c_list = [['Node Name','Eigenvector Centrality']]
for i in sorted_ec:
    temp_list = []
    temp_node_name = i
    temp_list.append(temp_node_name)
    
    temp_node_ec = eigen_centrality[temp_node_name]
    temp_list.append(temp_node_ec)
    eigen_c_list.append(temp_list)
    
print(tabulate(eigen_c_list,headers='firstrow', tablefmt='fancy_grid'))


# In[153]:


deg_centrality = nx.degree_centrality(G)

sorted_dc = sorted(deg_centrality)

deg_c_list = [['Node Name','Degree Centrality']]
for i in sorted_dc:
    temp_list = []
    temp_node_name = i
    temp_list.append(temp_node_name)
    
    temp_node_dc = deg_centrality[temp_node_name]
    temp_list.append(temp_node_dc)
    deg_c_list.append(temp_list)
    
print(tabulate(deg_c_list,headers='firstrow', tablefmt='fancy_grid'))


# In[154]:


total_degree = G.degree(G)
total_out_degree=G.out_degree(G)
total_in_degree=G.in_degree(G)


# In[155]:


degree_list = [['Node Name','Degrees','In-Degree','Out-Degree']]
for i in total_degree:
    temp_list = []
    temp_node_name = i[0]
    temp_list.append(temp_node_name)
    
    temp_node_degree = total_degree[temp_node_name]
    temp_list.append(temp_node_degree)
    
    temp_node_out = total_out_degree[temp_node_name]
    temp_list.append(temp_node_out)
    
    temp_node_in = total_in_degree[temp_node_name]
    temp_list.append(temp_node_in)
    degree_list.append(temp_list)

print(tabulate(degree_list,headers='firstrow', tablefmt='fancy_grid'))


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




