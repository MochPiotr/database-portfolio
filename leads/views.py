from django.db.models import Sum, Count, Value
from django.db.models.functions import Coalesce
from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic
from agents.mixins import OrganisorandLoginRequiredMixin
from .models import Lead, Agent, Category, Deal, Contact, UserProfile
from .forms import LeadForm, LeadModelForm, CustomUserCreationForm, AssignAgentForm, LeadCategoryUpdateForm, DealModelForm, ContactModelForm




class SignupView(generic.CreateView):
    template_name ="registration/signup.html"
    form_class = CustomUserCreationForm
    
    def get_success_url(self):
        return reverse("login.html")

class DashboardView(generic.TemplateView):
    template_name="dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user


        leads = Lead.objects.all()
        deals = Deal.objects.all()

        #if user.is_organisor:
        #    leads = Lead.objects.filter(organisation=user.userprofile)
        #    deals = Deal.objects.filter(lead__in=leads)
        #else:
        #    leads = Lead.objects.filter(organisation=user.agent.organisation)
        #    deals = Deal.objects.filter(lead__in=leads)

        context["leads"] = leads
        context["leads_count"] = leads.count()
        context["deals_count"] = deals.count()
        total_value = deals.aggregate(total=Sum("value")/1)["total"] or 0
        context["deals_total_value"] = total_value

        won_deals = deals.filter(status="Won").aggregate(total=Sum("value"))["total"] or 0
        lost_deals = deals.filter(status="Lost").aggregate(total=Sum("value"))["total"] or 0
        if lost_deals == 0:
            conversion_rate = 100
        else:
            conversion_rate = won_deals/lost_deals
        context['conversion_rate'] = conversion_rate

        top_deals = (
        Deal.objects
        .select_related("lead")
        .order_by("-value")[:5]
        )

        context["top_deals"] = top_deals

        return context


class LandingPageView(generic.TemplateView):
    template_name = "landing.html"

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        error = None

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error = "Incorrect Username or Password"
    
        context = self.get_context_data(error=error, username=username)
        return self.render_to_response(context)


def landing_page(request):
    return render('landing.html')

class LeadsView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/leads.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user

        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile,
                agent__isnull=False
            )
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation,
                agent__isnull=False,
                agent__user=user
            )



        # Tu dodajemy sumę wartości powiązanych dealów
        queryset = queryset.annotate(total_value=Sum("deals__value"))
        queryset = queryset.annotate(total_deals=Count("deals"))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # ⚠️ Nie nadpisujemy context["leads"], bo tracisz total_value!
        # Jeśli chcesz dodać coś więcej, zrób to obok:
        if user.is_organisor:
            context["unassigned_leads"] = Lead.objects.filter(
                organisation=user.userprofile,
                agent__isnull=True)
            
        return context


#class LeadListView(LoginRequiredMixin, generic.ListView):
  #  template_name = "leads/lead_list.html"
   # context_object_name = "leads"

#    def get_queryset(self):
 #       user = self.request.user

  #      if user.is_organisor:
   #         queryset = Lead.objects.filter(
    #            organisation=user.userprofile,
     #           agent__isnull=False
     #       )
     #   else:
     #       queryset = Lead.objects.filter(
     #           organisation=user.agent.organisation,
     #           agent__isnull=False,
     #           agent__user=user
     #       )
#
 #       queryset = queryset.annotate(total_value=Sum("deals__value"))
  #      return queryset
#
 #   def get_context_data(self, **kwargs):
  #      print("=== get_context_data wywołane ===")
   #     context = super().get_context_data(**kwargs)
#        user = self.request.user
#
#
#
 #       if user.is_organisor:
  #          context["unassigned_leads"] = Lead.objects.filter(
   #             organisation=user.userprofile,
    #            agent__isnull=True
     #       )
##       print("DEBUG leads queryset:", list(self.get_queryset().values("name", "total_value")))
  #      return context




class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name ="leads/lead_detail.html"
    context_object_name = "lead"
    def get_queryset(self):
        user = self.request.user 

        #initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation = user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation = user.agent.organisation)
            #filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pobranie wszystkich dealów przypisanych do tego leadu
        context['deals'] = Deal.objects.filter(lead=self.object)
        return context

def lead_detail(request, pk):
    print(pk)
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead
    }
    return render(request, "leads/lead_detail.html", context)


class LeadCreateView(LoginRequiredMixin, generic.CreateView):
    template_name ="leads/lead_create.html"
    form_class = LeadModelForm
    
    def get_success_url(self):
        return reverse("leads:leads")
    
    def form_valid(self, form):
        # TO DO send email
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()
        return super().form_valid(form)



def lead_create(request):
    form = LeadModelForm()
    if request.method == "POST":
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/leads')
    context = {
        "form": form
    }
    return render(request, "leads/lead_create.html", context)


class DealCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "leads/deal_create.html"
    form_class = DealModelForm

    def get_success_url(self):
        return reverse("deals")  # upewnij się, że taki URL name istnieje

    def form_valid(self, form):
        deal = form.save(commit=False)

        # przypisz organizację do deal.lead (jeśli chcesz, by każdy deal należał do jednej organizacji)
        if self.request.user.is_authenticated:
            deal.lead.organisation = self.request.user.userprofile
            deal.lead.save()

        deal.save()
        return super().form_valid(form)
    



class ContactCreateView(LoginRequiredMixin, generic.CreateView):
    template_name ="leads/contact_create.html"
    form_class = ContactModelForm
    
    def get_success_url(self):
        return reverse("contacts")
    
    def form_valid(self, form):
        contact = form.save(commit=False)  # Tworzy obiekt, ale jeszcze go nie zapisuje do bazy
        contact.organisation = self.request.user.userprofile  # przypisanie organizacji
        contact.save()  # zapis do bazy
        return super().form_valid(form)
    
def contact_create(request):
    form = ContactModelForm()
    if request.method == "POST":
        form = ContactModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/leads')
    context = {
        "form": form
    }
    return render(request, "contact_create.html", context)

class ContactDetailView(LoginRequiredMixin, generic.DetailView):
    template_name ="leads/contact_detail.html"
    context_object_name = "contact"
    def get_queryset(self):
        user = self.request.user 

        queryset = Contact.objects.filter(organisation = user.userprofile)


        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pobranie wszystkich dealów przypisanych do tego leadu
        #context['contacts'] = Contact.objects.filter(contact=self.object)
        return context

class ContactUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name ="leads/contact_update.html"

    form_class = ContactModelForm
    def get_queryset(self):
        user = self.request.user 
        return Contact.objects.filter(organisation = user.userprofile)

    def get_success_url(self):
        return reverse("contact-detail", kwargs={"pk": self.get_object().id})

class ContactDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name ="leads/contact_delete.html"
    
    def get_queryset(self):
        user = self.request.user 

        queryset = Contact.objects.filter(
                organisation = user.userprofile, 
                agent__isnull=False
                )
       
        return queryset
    
    def get_success_url(self):
        return reverse("contacts")

class LeadUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name ="leads/lead_update.html"
    form_class = LeadModelForm
    def get_queryset(self):
        user = self.request.user 
        return Lead.objects.filter(organisation = user.userprofile)
        


    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().id})


def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('/leads')
    context = {
        "form": form,
        "lead": lead
    }
    return render(request, "leads/lead_update.html", context)


class LeadDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name ="leads/lead_delete.html"
    
    def get_queryset(self):
        user = self.request.user 

        #initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation = user.userprofile, 
                agent__isnull=False
                )
        else:
            queryset = Lead.objects.filter(
                organisation = user.agent.organisation, 
                agent__isnull=False
                )
            #filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset
    
    def get_success_url(self):
        return reverse("leads:leads")


def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')


class AssignAgentView(OrganisorandLoginRequiredMixin, generic.FormView):
    template_name ="leads/assign_agent.html"
    form_class = AssignAgentForm 

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update ({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("leads:leads")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent 
        lead.save()
        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation = user.userprofile
                )
        else:
            queryset = Lead.objects.filter(
                organisation = user.agent.organisation
                )

        context.update({
            "unassigned_lead_count": queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user 

        #initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation = user.userprofile
                )
        else:
            queryset = Category.objects.filter(
                organisation = user.agent.organisation
                )
        return queryset
    
class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"


    def get_queryset(self):
        user = self.request.user 

        #initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation = user.userprofile
                )
        else:
            queryset = Category.objects.filter(
                organisation = user.agent.organisation
                )
        return queryset
    

class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name ="leads/lead_category_update.html"
    form_class = LeadCategoryUpdateForm
    def get_queryset(self):
        user = self.request.user 

        #initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation = user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation = user.agent.organisation)
            #filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset
        


    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().id})
    

class DealListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/deals.html"
    context_object_name = "deal_list"

    def get_queryset(self):
        user = self.request.user 
        queryset = Deal.objects.all()


       # if user.is_organisor:
       #     queryset = Deal.objects.filter(lead__organisation=user.userprofile)
       # else:
       #     queryset = Deal.objects.filter(lead__organisation=user.agent.organisation)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        top_deals = (
        Deal.objects
        .select_related("lead")
        .order_by("-value")[:5]  
    )

        context["top_deals"] =  top_deals

        



        total_created = Deal.objects.filter(status="Created").aggregate(total=Sum("value"))["total"]
        total_created_count = Deal.objects.filter(status="Created").aggregate(total=Count("value"))["total"]
        
        total_in_progress = Deal.objects.filter(status="In Progress").aggregate(total=Sum("value"))["total"]
        total_in_progress_count = Deal.objects.filter(status="In Progress").aggregate(total=Count("value"))["total"]

        total_lost = Deal.objects.filter(status="Lost").aggregate(total=Sum("value"))["total"]
        total_lost_count = Deal.objects.filter(status="Lost").aggregate(total=Count("value"))["total"]

        total_won = Deal.objects.filter(status="Won").aggregate(total=Sum("value"))["total"]
        total_won_count = Deal.objects.filter(status="Won").aggregate(total=Count("value"))["total"]


        context["total_created"] = total_created or 0
        context["total_created_count"] = total_created_count or 0

        context["total_in_progress"] = total_in_progress or 0
        context["total_in_progress_count"] = total_in_progress_count or 0

        context["total_lost"] = total_lost or 0
        context["total_lost_count"] = total_lost_count or 0

        context["total_won"] = total_won or 0
        context["total_won_count"] = total_won_count or 0

        return context

    def get_success_url(self):
        return reverse("leads:lead-deal")

class DealDetailView(LoginRequiredMixin, generic.DetailView):
    template_name ="leads/deal_detail.html"
    context_object_name = "deal"
    def get_queryset(self):
        user = self.request.user 

        queryset = Deal.objects.all()


        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pobranie wszystkich dealów przypisanych do tego leadu
        #context['contacts'] = Contact.objects.filter(contact=self.object)
        return context

class DealUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name ="leads/deal_update.html"
    form_class = DealModelForm
    def get_queryset(self):
        user = self.request.user 
        return Deal.objects.all()
        


    def get_success_url(self):
        return reverse("leads:deal-detail", kwargs={"pk": self.get_object().id})

class DealDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name ="leads/deal_delete.html"
    
    def get_queryset(self):
        user = self.request.user 

        queryset = Deal.objects.all()
       
        return queryset
    
    def get_success_url(self):
        return reverse("deals")


class ContactListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/contacts.html"
    context_object_name = "contacts"

    def get_queryset(self):
        # Pobiera wszystkie kontakty i dodaje do każdego pola total_value i total_deals
        return Contact.objects.annotate(
            total_value=Sum("deals__value"),
            total_deals=Count("deals")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # kontakty już zawierają sumy i liczby dealów
        context["contacts"] = self.get_queryset()
        return context
    
#def lead_update(request, pk):
#    lead = Lead.objects.get(id=pk)
#    form = LeadForm()
#    if request.method == "POST":
#        form = LeadForm(request.POST)
#        if form.is_valid():
#            first_name = form.cleaned_data['first_name']
#            last_name = form.cleaned_data['last_name']
#            age = form.cleaned_data['age']
#            lead.first_name = first_name
#            lead.last_name = last_name
#           lead.age = age
#            lead.save()
#            return redirect('/leads')
#    context = {
#        "form": form,
#        "lead": lead
#    }
#    return render(request, "leads/lead_update.html", context)


#def lead_create(request):
 #   form = LeadForm()
  #  if request.method == "POST":
   #     print('Receiving a post request')
    #    form = LeadForm(request.POST)
     #   if form.is_valid():
      #      print("The form is valid")
      #      print(form.cleaned_data)
      #      first_name = form.cleaned_data['first_name']
      #      last_name = form.cleaned_data['last_name']
      #      age = form.cleaned_data['age']
      #      agent = Agent.objects.first()
      #      Lead.objects.create(
      #          first_name=first_name,
      #          last_name=last_name,
      #          age=age,
      #          agent=agent
      #      )
      #      print("The lead has been created")
      #      return redirect('/leads')
    #context = {
     #   "form": form
    #}
    #return render(request, "leads/lead_create.html", context)