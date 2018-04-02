from TwitterAPI import TwitterAPI
from django import shortcuts
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView
from rest_framework.response import Response
from rest_framework.views import APIView
from yelpapi import YelpAPI

from displays.forms import BoxForm, DisplayForm
from models import Display, Box, Element, Picture
from panel.views import ExtendModelCrud, MessageCreateView, MessageUpdateView, LoginReqListView
from products.models import Category, Product
from .response import JSONResponse, response_mimetype
from .serialize import serialize


class PictureCreateView(CreateView):
    model = Picture

    def form_valid(self, form):
        self.object = form.save()
        files = [serialize(self.object)]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class PictureListView(ListView):
    model = Picture

    def render_to_response(self, context, **response_kwargs):
        qs = self.get_queryset().filter(box=self.kwargs['pk'])
        files = [serialize(p) for p in qs]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
        # def get_queryset(self,**kwargs):
        #     qs = super(PictureListView, self).get_queryset()
        #     list = qs.filter(box=self.kwargs['pk'])
        #     return list


class PictureDeleteView(DeleteView):
    model = Picture

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response = JSONResponse(True, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class BasicVersionCreateView(PictureCreateView):
    template_name_suffix = '_basic_form'


class DisplayListView(ListView):
    model = Display
    template_name = 'display_list.html'


class DisplayCreateView(MessageCreateView):
    form_class = DisplayForm


class BoxCreateView(MessageCreateView):
    form_class = BoxForm


class DisplayUpdateView(MessageUpdateView):
    form_class = DisplayForm


class DisplayCrud(ExtendModelCrud):
    list_class_view = DisplayListView
    create_class_view = DisplayCreateView
    update_class_view = DisplayUpdateView


display_crud = DisplayCrud(
        model=Display,
        fields=('name', 'background_color'),
        info_fields=('id', 'name', 'background_color')
)


class BoxListView(LoginReqListView):
    model = Box


class BoxCreateView(MessageCreateView):
    form_class = BoxForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            box = form.save(commit=False)
            element = Element()
            element.type = 2
            element.value = -1
            element.save()
            box.element = element
            box.save()
            return shortcuts.redirect(self.get_success_url())
        return super(BoxCreateView, self).post(request, *args, **kwargs)


class BoxUpdateView(MessageUpdateView):
    form_class = BoxForm


class BoxCrud(ExtendModelCrud):
    list_class_view = BoxListView
    update_class_view = BoxUpdateView
    create_class_view = BoxCreateView


box_crud = BoxCrud(
        model=Box,
        fields=('id', 'display', 'row', 'col', 'size_x', 'size_y', 'background_color'),

)


class ElementListView(ListView):
    model = Box


class ElementCrud(ExtendModelCrud):
    list_class_view = ElementListView


element_crud = BoxCrud(
        model=Element,

)


class TweetList(APIView):
    def post(self, request):
        api = TwitterAPI('onbs4DFcj5QYmdpRUeGm5ZTvG', 'vvqKKVwh4VQCLbXbKyr7n5ByE4zvzbsSLoWEIvug5f5CvoRsGu',
                         '112813592-Pms9mQHdu9VfJ7V2mrWtHa4gDHV7YB6Dfv1O4JS9',
                         '9gn8Wsgw4e9KOUngtLCGWTU34RLJIF7j2xMyWP9LLNZAK')
        r = api.request('statuses/user_timeline', {'screen_name': request.DATA.get('name')})
        return Response({'tweets': r.get_iterator().results})


class YelpReviewList(APIView):
    def post(self, request):
        yelp_api = YelpAPI('4eeWvgRSP72tOmZaghWTvQ', 'K88plDw1UnwjACzBophf6Du578c', 'uKfMmBjcu1_JXCj5aS1o9foFOB8VpN4q',
                           'DRi5uRtvXpyXSRUxhf_8SaQ52LI')
        search_results = yelp_api.business_query(request.DATA.get('name'))
        return Response({'results': search_results.get('reviews')})


class LastCheckIn(APIView):
    def get(self, request):
        pass

    def post(self, request):
        return Response()


class CategoryProductList(APIView):
    def post(self, request):
        category = Category.objects.get(name=request.DATA.get('name'))
        data = {}
        data['products'] = []
        for product in category.products.all():
            if product.image:
                data['products'].append(
                        {'product': {'price': product.price, 'name': product.name, 'image': product.image.url}})
        return Response(data=data)


class ProductView(APIView):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return Response({'image': product.image.url, 'price': product.price, 'name': product.name})


def weather(request, zip):
    url = request.POST.get('url')
    import urllib2
    from django.http import HttpResponse
    import mimetypes
    try:
        proxied_request = urllib2.urlopen(url)
        status_code = proxied_request.code
        mimetype = proxied_request.headers.typeheader or mimetypes.guess_type(url)
        content = proxied_request.read()
    except urllib2.HTTPError as e:
        return HttpResponse(e.msg, status=e.code, mimetype='text/plain')
    else:
        return HttpResponse(content, status=status_code, mimetype=mimetype)
        # return render_to_response('displays/weather.html',{'json':json.dump(content)}, context_instance=RequestContext(request))
