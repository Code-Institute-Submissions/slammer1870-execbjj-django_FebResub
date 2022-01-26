from django.shortcuts import render, redirect

# Create your views here.
def terms_and_conditions(request):
    return render(request, "terms_and_conditions.html")

def privacy_policy(request):
    return render(request, "privacy_policy.html")