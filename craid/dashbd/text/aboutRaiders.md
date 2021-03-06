
## FAQ

### Joining The Fight

1. Much of ClubRaiders activity is coordinated on the [Pleiades Historical Society discord](https://discord.gg/PdaCsRA).  All commanders are welcome.  There, you can 
 * join existing actions with other commanders, 
 * create a new action of your own, 
 * learn more about The Club in the extensive library, 
 * and discuss the project with commanders with a wide range of experience from squadrons spanning the populated galaxy.
2. Interested in building an Anti-Club Squadron from the ground up?  The Pleiades Historical Society (PLOR) is a fledgling squadron
dedicated to removing The Club from the Pleiades and solving the remaining mysteries at play in the region.
3. PHS has written a useful guide [How to Retreat a Minor Faction](https://docs.google.com/document/d/1gP8cRjFQGlzH-HcQj1vIKJMLSi9h0i7qHvggL39A618/edit#).
4. Squadrons - want to help but not spend any manpower?  Identify the Club factions in your area and ask your squadron-mates not to do anything for these factions.

### Using the site

1. I want to discuss an issue.
    * [There is now a forum thread on Frontier Development's web site](https://forums.frontier.co.uk/threads/club-raiders-fighting-the-club-in-the-bgs.548972).  If you are
    a Discord user, feel free to join us at https://discord.gg/6TWATZF
1. How do you identify club-related minor factions?
    * They were identified by [The Children of Raxxla](https://inara.cz/squadron/4980/) in [The Holdstock Report](https://docs.google.com/document/d/1MPw1EzRmor2TvRw97QvB8lNTcBT2XffrMuMwEOAXaW8/edit?usp=sharing).
    There's a big diagram on the "About The Club" tab that shows the conclusions in an accessible way.
1. How about player minor factions?
    * They are explicitly filtered out of consideration.  We had one case where a player minor faction
    wasn't identified as such on http://eddb.io.  In that case, someone should fix the faction on Eddb and
    changes will be reflected here in a day or so.
1. How is difficulty calculated?
    * difficulty = (population / 15000.0) * (influence^2) / 1000.0
    * for factions that cannot be forced to retreat, difficulty is 999999
    * the formula was chosen so that a value of 1 would be about right for a
        single commander and 100 would be about right for a small group or
        a valiant single effort.
    * some combinations that give a difficulty of around 1.0 are 25inf/25,000pop,
        8inf/250,000pop and 3.5inf/1,200,000pop.
       
### The Elite Background Simulation (BGS)

1. I want to learn more about the BGS.
    * The BGS is an almost-wholly undocumented, often misunderstood game that is frustrating to many.  There
       are many sources of information on it.  The "Elite BGS" Discord, linked on the main page is a premiere
       source of information, with a full bibliography.  https://forums.frontier.co.uk/threads/dont-panic-bgs-guides-and-help.400110/
       is also good place to read up and talk about the BGS.
 
### Improving the site 

1. Numbers in the table should be formatted better.
    * We're waiting on a bug fix in Dash.
1. I have a better sort query/filter query for an activity or want to add a new activity.
    * This sort of issue can be expressed on the channels mentioned above.  There's plenty of room for tweaking and improvements.
1. I want to add or change some text.
    * There are two ways: one is to get added to the project on Github and the second is to talk
    to someone who is added to the project on Github.  You can join Github here: https://help.github.com/en/github/getting-started-with-github/signing-up-for-a-new-github-account
1. I want to report a bug.
    * https://github.com/HausReport/ClubRaiders/issues is the best place.  Discord and the Frontier forum
    thread also work.
    
### About the program

1. Tell me about the program.
    * It's open-source, written in Python using Plotly's Dash framework. 
    The source code is available at https://github.com/HausReport/ClubRaiders.
1. I'm a programmer and I want to work on the code.
    * By all means, give me a shout on Github.
1. I'm a programmer and I want to use the code.
    * By all means, the license is a very easy-to-satisfy BSD-3 clause.
        
