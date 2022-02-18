# Reddit Bot
I started this project with the goal of tracking some of the top posts of the day and keeping tabs on users that consistently were able to break into those top posting spots. The idea being that this might be a way to identify, if not just power users, repost and karma farming bots and the like. However, the core of the project became a little bit more generic as a couple of ideas crystallized and the original bot became more of a generic platform upon which other ideas could be built.

# Parser Bot
This bot scans post comments and aggregates keywords above a certain threshold. A long term goal will be to create output that can be integrated into a dashboard and track sentiment over time.

# "This!" Bot
This bot scans the top Reddit posts of the day looking for any comments that begin with "This." Once the bot finds such a comment, it sarcastically prints out the reply to console "This! This right here!"

In the future, methods could be added to reply to the inciting user's post with the text, but this would very likely get the bot banned as it adds very little to the discussion in any given context. 

Sample output:
![image](https://user-images.githubusercontent.com/91224707/153680492-bb58a36a-468f-4daf-94eb-b411d3fdbd26.png)

![image](https://user-images.githubusercontent.com/91224707/153680915-b41e0205-a473-4941-ad88-ac750bf6afe0.png)
