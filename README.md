# Personal-information-manager-webapp

# Introduction

The repository contains a web app to create and maintain personal notes. The following
features are supported
<ul>
  <li>View notes</li>
  <ul>
    <li>See all the notes. Sorted by date.</li>
    <li>Click on a note to see details</li>
    <li>Edit the title, text or hashtags of the note</li>
  </ul>
  
  <li>Search views</li>
  <ul>
    <li>List of all hashtags. If you click on one, you can see all notes with that
      hashtag</li>
    <li>Search box. You can enter a word and hit enter to see all notes which
      have that word. Similar to the “see all notes” view</li>
  </ul>
</ul>
   
# Setting up

1. Clone repository
   1.  Create a virtualenv and activate it
1. Install dependencies using `pip install -r requirements.txt`
1. create postgres db "pim" in sqlterminal using "CREATE DATABASE pim;"
1. `export FLASK_APP=pim_app` to set the application
1. `flask initdb` to create the initial database
1. `flask run` to start the app.

