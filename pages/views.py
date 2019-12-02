from django.shortcuts import render, render_to_response, redirect
from django.views.generic import TemplateView, View, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, SearchForm
from bokeh.layouts import column
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.resources import INLINE
import random, tweepy

# create views here
class HomeView(TemplateView):

    #get method decides weather to transition
    #to results or stay on the home page
    def get(self, request):
        form = SearchForm()
        context = {
            'title': 'Home',
            'status0': 'active',
            'form': form,
        }
        return render(request, 'home.html', context)

    def post(self, request):

        form = SearchForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['search']

            #need to move this chunk of code
            auth = tweepy.OAuthHandler('gD2XB4HhO4hQOFoc9OMSVIcMV', 'mS5GZ2eJaSIcJIxF5w9iRWx6sglfQzMGcbmiL6Rrrl3K125vYo')
            auth.set_access_token('1188574858571059200-BBWOHfZBmJu4IrrkpS90gFKgS04c8s', 'q2zccyrkuUr9rThgkZmsLtYPxhQoAK1gouwXUHJOKGiGR')
            api = tweepy.API(auth)
            tweet_list = []
            for tweet_info in tweepy.Cursor(
                    api.search,
                    q = text,
                    tweet_mode = 'extended',
                    lang = 'en').items(20):
                if 'retweeted_status' in dir(tweet_info):
                    tweet = tweet_info.retweeted_status.full_text
                else:
                    tweet = tweet_info.full_text
                tweet_list.append(tweet)


            context = {
                'title': 'Results',
                'text': text,
                'tweets': tweet_list,
            }
            return render(request, 'bokeh.html', context)

class AboutView(View):

    def get(self, request):
        context = {
            'title': 'About',
            'status1': 'active',
        }
        status = 'active'
        return render(request, 'about.html', context)

class SignUp(generic.CreateView):

    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class ResultsView(TemplateView):

    #get method for generating the graph display
    def post(self, request):

        #randomly generated x coord and y coord
        x_coord = []
        y_coord = []
        for i in range(100):
            x_coord.append(random.randint(0,50))
            y_coord.append(random.randint(0,50))

        #create scatter plot for figure 1
        plot = figure(
            title='Test Scatter',
            x_axis_label='X-axis',
            y_axis_label='Y-axis',
            plot_width=400,
            plot_height=400,
            sizing_mode='scale_width'
            )

        plot.scatter(x_coord,y_coord)

        #define line graph coords
        x1 = [1,2,3,4,5]
        y1 = [1,2,3,4,5]

        #plot as line graph figure 2
        plot1 = figure(
            title='Test Line',
            x_axis_label='X-axis',
            y_axis_label='Y-axis',
            plot_width=400,
            plot_height=400,
            sizing_mode='scale_width'
            )
        plot1.line(x1,y1,line_width=2)

        #assign both craphs to a column structure
        col = column([plot,plot1],sizing_mode='scale_width')

        script, div = components(col)

        #containing items to be returned to html 
        context = {
            'resources': INLINE.render(),
            'title': 'Results',
            'script': script, 
            'div': div
        }

        #return request with correct html along wiht context
        return render(request,'bokeh.html',context)
