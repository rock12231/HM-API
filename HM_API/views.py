from django.http import HttpResponse


def APIRunning(request):
    return HttpResponse('''<br><br><br><br><br><br><center><h1><b>🥳🥳🥳 !!! WoW After One Year OMG !!! 🥳🥳🥳</b></h1><center><br><br> <center>Hey everyone,

I'm thrilled to announce that my API is now live on Render.com! 🥳 It's been an amazing journey building this project, and I'm so excited to share it with the world.

Deploying on Render was a breeze! Their platform made it incredibly easy to set up my environment and get my API up and running in no time. Plus, with their free plan, I can start small and scale as needed, which is perfect for my project.

If you're looking to deploy your API or any other project, I highly recommend giving Render a try. The experience has been fantastic, and I can't wait to see what else I can build with their platform.

Check out my API live at your-api-url-here and let me know what you think! 🚀

Cheers to new beginnings and exciting deployments!<center>''')