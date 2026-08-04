# Research Blog

Add a new entry each week (or more often if you like). Be honest — write what actually happened, not just what went well. This log will help you write your final report.

---

## YYYY-MM-DD

**What I worked on:**
_Describe the main tasks, experiments, or analyses you did this week._

**What helped:**
_A paper, a conversation with your mentor, a tutorial, a tool — what moved you forward?_

**What was challenging:**
_A bug, a confusing result, something you couldn't figure out — write it down even if unresolved._

**What I learned:**
_One or two things you understand better now than you did last week._

### Log
## 2026/05/29
This week I was able to read through papers and documents pertaining to RadClss, Py-ART, MC3E, github, etc.
I was also able to somewhat navigate the github repository and commit a test text file to my fork of the 
repository. Earlier in the week I attended both orientation sessions and had a meeting with Joseph about 
the scope of the project and what are some of the next steps going forward. 

The paper describing how to navigate and use github was really helpful in understanding the basics of how to
use github. 

Getting github set up on my computer and trying to commit files to github was challenging. I also had issues
with the subsystem that was setup on the office computer which may need to be resolved sooner rather than later.

I now do have a better understanding of operating and using github and I also learned more about the MC3E feild
campaign and RadClss software which will both be very important going forward.

Plan for this next week is to set up coding environment, plot radar data with aircraft overlays from the May 
20th event, make GIFS for that associated event, and if time allows work on incorporating those GIF images 
into the GUI that was being developed by Christian.

## 2026/06/05
This week I worked mainly on getting more familiar with the Py-ART code and a lot of different cool methods for 
plotting radar data. Half way through the week I was able to get a hold of radar data from C-SAPR during the time
of the MC3E field campaign around the May 20, 2011 day. I was also able to locate flight data for this day which 
led me to making a bunch of gifs that showed not only just the C-SAPR radar data but also overlayed flight tracks
during this day too. This has allowed me to have multiple code files that all have little bits and pieces that will
be useful for making the final Rad-CAT product.

Having a couple of conversations with Joe helped me locate alot of different data that was important for going 
forward in the writting of code. 

Locating the data was very challenging as none of the data was in one nice place and thus resulted in a lot of time
spent trying to not only find the data but also being able to download it was a challenge in itself...

I have learned better how to use the Py-ART library and also am more able and comfortable in navigating the github 
repository. 

## 2026/06/12
This week I worked on code that would find which elevation sweep the Citation aircraft was in and then would plot a ppi 
of just that sweep along with code that would generate a sudo RHI scan of the vertical cross section that the aircraft 
was in. Then I was able to find the data file containing all of the cloud microphysics observations from the citation
and display some of the parameters and compare them with some of the reflectivity values that I earlier found. I also 
worked on code that would create a time series plot of radar reflectivity above, on, and below the aircraft based on
its location and then add that extra data into the data array containing the other microphysics data. Then as of more 
recent I have been working on and will still be finishing up figure creation of sudo RHI scans to then compare some of 
these with the data that I am extracting. I also started on a draft of the introduction to the final SULI paper too.

Something that was and still is confusing is matplotlib not fully plotting my 10 second interval data, my guess is it has
something to do with how matplotlib is defining intervals and how my intervals are but I am not for sure. 

I have definetly become more comfortable with retrieving data from the ARM data base as I was more easily able to get the
citation observation data this time around. 

Next week I will try to finish up the sudo RHI images for comparison and I would also like to talk with Joe further 
about my methodology of data extraction to make sure that the method makes sense. 

## 2026/06/19
This week I finished generating a sample set of sudo RHI images to compare these with the columnar vertical profile 
extraction where in which they seemed to be very similar to each other. Then I started to work on a four panel display
of radar PPI scans with aircraft location, HVPS-3 particle images, flight altitude over time, and particle size 
distribution. I was also able to get a formula down for converting particle size distribution to sudo radar reflectivity 
for further comparison between radar and aircraft measurements. I also worked a bit on the final paper methodology and 
introduction where Joe gave some feedback. My next steps will be getting a full data set of radar reflectivity for the 
citations location and then comparing radar reflectivity with the sudo reflectivity found. I will also work on a 
classification system to differentiate what the aircraft is doing at certain times in order to compare reflectivities at 
certain legs of the flight. 

A difficulty that I ran into was the my data isn't seeming to align up when I parse through it and I hope to eventually
find an answer to that issue but in the mean time I will just be mindful that my data might be off. 

I found that there hasn't been much work done with sudo reflectivity comparisons to radar reflectivity. I also learned that
when doing these comparisons there is a dieletric coefficient that can be applied that does seem to correct the data and 
gives a very reasonable result. 

Next week I plan to work on finishing up the ppi with aircraft images for the four panel display and also finishing up
the analysis between the sudo and radar reflectivity. I would also like to work more on the papers introduction and 
methodology along with maybe start the poster??

## 2026/06/26
This week I mostly worked on a functional interactive four panel display of the UND aircraft overlayed on a PPI map 
along with HVPS-3 particle images, aircraft altitude and temperature time series, and particle size distribution 
observed by the HVPS-3. This is mostly completed now with just a few finishing touches that will probably take place next 
week to then generate some figures for the SULI poster and maybe paper figures. I was also able to start work on a third 
draft of the SULI paper introduction implementing the changes that Joe had suggested along with some flow improvements too.
I was also able to get a basic generation of phase clasification added to the aircraft microphysics file so that now there 
can be some comparison done with what the aircraft is observing and what the CSU radar tools is claiming that the radar is 
theoretically seeing in that given area. Based upon some quick analysis of what was being shown in this comparison there 
does deffinetly seem to be some discrepancies between the in-situ and remote sensing datas. 

A difficulty that I ran into this week was an issue where when on the CELS compute server when I would try to generate the
PPI scans with aircraft overlay there were some weird issues with the aircraft and radar locations seeming to not be correct 
to what the data array claims to have in it. This seems like it might be an issue with the cartopy library that is on the server
but I am unsure. As a fix to this I just generated the PPI scans locally on my own computer where the data would seemingly plot
correctly. Another oddity that I came across was when plotting a comparison of the radar reflectivity and the aircraft sudo 
reflectivity there seemed to be a logarithmic difference between the two which will need to be looked more in to in the future 
so that proper analysis of these variables can be done. 

Next week I plan to work on the SULI paper some more along with getting some considerable work done to the poster. I will also
be doing some touch ups to the four panel display and some futher comparison of HVPS-3 observations and CSU radar tools 
hydrometeor classification at some different aircraft locations. I would also like to get a considerable amount of figures prepared
for the poster this next week if I am unable to do much else with the poster given time constraints. 

## 2026/07/02
This week I was able to finish up some more analysis of data after running the phase classification algorithm. Joe and I also were 
able to formalize what I will be focusing on in the poster which will be hail events and how well they are being classified as 
after some short analysis it was found that the events seem to not be getting classified really well. Also there seems to be a better
explaination as to why the radar reflectivity and calculated reflectivity are off and that is most likely do to the sizing algorithm
where elongated objects when a best fit circle is placed around them will underestimate the size of the object. I was also able to 
find that only during flight levels above 5000m is the aircraft calculated reflectivity at least within 5 dBz of the radar reflectivity
and this is seemingly due to the fact that the particles observed above 5000m are perfect small spheres that are completely ice. 
I was also able to work a lot on the SULI paper introduction and have a better idea of the flow that I will be working on going into 
next week. I was somewhat able to work on the poster, I got most of the figures generated but mostly just need to start the writing 
process. 

Next week I plan to work more on the paper and poster with more emphasis on the poster as the due date for that is coming up. In terms 
of analysis of data it seems that is winding down so from here on I will plan to just mess around with data at any points of free time 
that I may get over the next couple of weeks. I also wouldn't mind working on another display for data that takes in a time and displays
particle images and a bunch of other microphysics data but time allowing we will see where I can get. 

## 2026/07/10
Throughout the week I mostly focused on getting the SULI poster done and working on more of the paper. I was able to get the poster mostly 
finished with just some small revisions needed that will be completed this next week. As for the paper I was able to get the introduction mostly 
finished along with a rough outline draft of the methodology. There was some analysis work done with regards to the project and now the plan is
to look at the possible chain aggregate cases that were present from the HVPS-3 images. This next week I plan to finish up the poster and the
introduction to the paper along with getting the methodology more nailed down. I will also start working on some more analysis of these possible
chain aggregate cases as the Cloud Imaging Probe was used on this campaign and will reveal if there really were chains present during the
May 20th flight.

## 2026/07/17
This week I was able to consalidate all of the RadCAT code into a python file that works by taking in the directory location of all the radar files
and the aircraft microphysics file and then returns a new microphysics file with hydrometeor classification and radar reflectivity of the respective
location of the aircraft. I was also able to complete the poster and submit it to its respective dropbox. There was a slight last minute change to 
the poster as we used a mass dimensional reflectivity calculation instead of the regular radar reflectivity equation. This resulted in a more 
linear trend but there was still underprediction between the calculated value and radar returned value for reflectivity. 

One main challenge that I ran into this week was that there was really not great clarification as to what all needed to be submitted this week, i.e. 
does the abstract need to be included with the poster when it is submitted and there was also alot of different places that said that things should be 
submitted in other locations then what was provided in emails. In the end I found out the the abstract does not need to be submitted with the poster 
and the poster only needs to be submitted to the dropbox in the Argonne box account. 

Plans for next week will mostly consist of working on the paper and possibly doing some more coding work to further consolidate and document different 
codes that were made throughout the extent of the internship. I may even start looking at some other campaigns are other case day of MC3E using the 
RadCAT analysis to start building a decent dataset before the internship concludes. 

## 2026/07/24
Throughout this week I worked on the SULI paper deliverable and was able to get most sections drafted. The only section left to finish a draft for is the 
conclusion, from which I will then plan to work on reviewing all the sections and making sure that the paper flows well. Some topics of discussion that 
came up between Joe and I was talking about a CPI imagery reconstruction algorithm that is being worked on by Columbia University and plans for a meeting 
with them to learn more about the software. We had also talked about AI and its general usefullness when it comes to coding projects that are easy but 
are also time consuming. Lastly I was able to upload all of the used data along with a majority of the figures from this summer to the GCE sever through
Argonne under the mc3e directory. 

Next week I plan to finish the paper before the July 31st deadline, I am also presenting at the CELS student poster session on Wednesday and will also 
be present at Learning on The Lawn at Argonne. After learning on the lawn I will finish up the peer review deliverable that is due and I will also plan 
to submit the general audience abstract that is already made up. 
---
