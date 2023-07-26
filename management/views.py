from django.utils import timezone
from datetime import date
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, login, logout, update_session_auth_hash
from django.core.mail import send_mail
from django.conf import settings

from .models import Citizen, CitizenAddress, CitizenParent, CitizenDocument, DocumentApplication, Service

# your views here.


def handle_not_found(request, exception):
    return render(request, 'page_404/404.html')


def home(request):
    # getting services
    ServiceData = Service.objects.filter()
    context = {
        'title': 'Welcome',
        'home_active': 'active',
        'serviceData': ServiceData
    }
    return render(request, 'management/home.html', context)


def contact_us(request):
    context = {
        'title': 'Contact us',
        'contact_active': 'active',
    }
    return render(request, 'management/contact.html', context)


def registrarLogin(request,):
    if not request.user.is_authenticated or request.user.is_registrar != True:
        if request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, email=email, password=password)

            if user is not None and user.is_registrar == True:
                login(request, user)
                messages.success(
                    request, ('Hi '+user.first_name+', Welcome back to the dashboard!'))
                return redirect(dashboard)
            else:
                messages.error(
                    request, ('User Email or Password is not correct! Try agin...'))
                return redirect(registrarLogin)
        else:
            context = {'title': 'Civil Registrar Login', }
            return render(request, 'management/registrar/login.html', context)
    else:
        return redirect(dashboard)


@login_required(login_url='registrar_login')
def registrarLogout(request):
    logout(request)
    messages.info(request, ('You are now Logged out.'))
    return redirect(registrarLogin)


@login_required(login_url='registrar_login')
def dashboard(request):
    if request.user.is_authenticated and request.user.is_registrar == True:
        # getting data
        citizens = Citizen.objects.filter()
        newApplications = DocumentApplication.objects.filter(
            status__isnull=True)

        context = {
            'title': 'Civil Registrar Dashboard',
            'dash_active': 'active',
            'citizens': citizens,
            'newApplications': newApplications,
        }
        return render(request, 'management/registrar/dashboard.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(registrarLogin)


@login_required(login_url='registrar_login')
def registrarProfile(request):
    if request.user.is_authenticated and request.user.is_registrar == True:
        if 'update_password' in request.POST:
            old_password = request.POST.get("old_pass")
            new_password = request.POST.get("pass1")
            confirmed_new_password = request.POST.get("pass2")

            if old_password and new_password and confirmed_new_password:
                user = get_user_model().objects.get(email=request.user.email)

                if not user.check_password(old_password):
                    messages.error(
                        request, "Your old password is not correct!")
                    return redirect(registrarProfile)

                else:
                    if len(new_password) < 5:
                        messages.warning(request, "Your password is too weak!")
                        return redirect(registrarProfile)

                    elif new_password != confirmed_new_password:
                        messages.error(
                            request, "Your new password not match the confirm password !")
                        return redirect(registrarProfile)

                    else:
                        user.set_password(new_password)
                        user.save()
                        update_session_auth_hash(request, user)

                        messages.success(
                            request, "Your password has been changed successfully.!")
                        return redirect(registrarProfile)

            else:
                messages.error(request, "Error , All fields are required !")
                return redirect(registrarProfile)

        else:
            newApplications = DocumentApplication.objects.filter(
                status__isnull=True)
            context = {
                'title': 'Registrar | Profile',
                'newApplications': newApplications,
            }
            return render(request, 'management/registrar/profile.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(registrarLogin)


@login_required(login_url='registrar_login')
def newApplication(request,):
    if request.user.is_authenticated and request.user.is_registrar == True:
        # getting new request
        newApplications = DocumentApplication.objects.filter(
            status__isnull=True)
        context = {
            'title': 'Registrar - New Document Requests',
            'request_active': 'open active',
            'newRequest_active': 'active',
            'newApplications': newApplications,
        }
        return render(request, 'management/registrar/application_list.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(registrarLogin)


@login_required(login_url='registrar_login')
def archivedRequest(request,):
    if request.user.is_authenticated and request.user.is_registrar == True:
        newApplications = DocumentApplication.objects.filter(
            status__isnull=True)
        # getting archived requests
        archivedRequests = DocumentApplication.objects.filter(
            status__isnull=False)
        context = {
            'title': 'Registrar - Archived Document Requests',
            'request_active': 'open active',
            'archived_active': 'active',
            'archivedRequests': archivedRequests,
            'newApplications': newApplications,
        }
        return render(request, 'management/registrar/archived_request.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(registrarLogin)


@login_required(login_url='registrar_login')
def services(request):
    if request.user.is_authenticated and request.user.is_registrar == True:
        if 'new_service' in request.POST:
            service_name = request.POST.get("service_name")
            description = request.POST.get("description")
            process_time = request.POST.get("process_time")
            service_fees = request.POST.get("service_fees")

            if service_name:
                # service_name=service_name.upper()
                found_data = Service.objects.filter(name=service_name)
                if found_data:
                    messages.warning(request, "The service " +
                                     service_name+", Already exist.")
                    return redirect(services)
                else:
                    # add new service
                    add_service = Service(
                        name=service_name,
                        description=description,
                        processingTime=process_time,
                        fees=service_fees
                    )
                    add_service.save()

                    messages.success(
                        request, "New Service created successfully.")
                    return redirect(services)
            else:
                messages.error(request, "Error , Service name is required!")
                return redirect(services)
        else:
            newApplications = DocumentApplication.objects.filter(
                status__isnull=True)
            # getting services
            ServiceData = Service.objects.filter()
            context = {
                'title': 'Registrar - Service List',
                'service_active': 'active',
                'services': ServiceData,
                'newApplications': newApplications,
            }
            return render(request, 'management/registrar/services.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(registrarLogin)


@login_required(login_url='registrar_login')
def servicesEdit(request, pk):
    if request.user.is_authenticated and request.user.is_registrar == True:
        service_id = pk
        # getting service
        if Service.objects.filter(id=service_id).exists():
            # if exists
            foundData = Service.objects.get(id=service_id)

            if 'update_service' in request.POST:
                # Retrieve the form data from the request
                service_name = request.POST.get('service_name')
                description = request.POST.get('description')
                process_time = request.POST.get("process_time")
                fees = request.POST.get("service_fees")

                if service_name:
                    if Service.objects.filter(name=service_name).exclude(id=service_id):
                        messages.warning(
                            request, "Service name already exist.")
                        return redirect(servicesEdit, pk)
                    else:
                        # Update Service
                        service_updated = Service.objects.filter(id=service_id).update(
                            name=service_name,
                            description=description,
                            processingTime=process_time,
                            fees=fees
                        )
                        if service_updated:
                            messages.success(
                                request, "Service "+service_name+", Updated successfully.")
                            return redirect(servicesEdit, pk)
                        else:
                            messages.error(request, ('Process Failed.'))
                            return redirect(servicesEdit, pk)
                else:
                    messages.error(request, ('Service name is required.'))
                    return redirect(servicesEdit, pk)

            elif 'delete_service' in request.POST:
                # Delete Service
                delete_service = Service.objects.get(id=service_id)
                delete_service.delete()
                messages.success(request, "Service info deleted successfully.")
                return redirect(services)

            else:
                newApplications = DocumentApplication.objects.filter(
                    status__isnull=True)
                context = {
                    'title': 'Registrar - Service Info',
                    'service_active': 'active',
                    'service': foundData,
                    'newApplications': newApplications,
                }
                return render(request, 'management/registrar/service_details.html', context)
        else:
            messages.error(request, ('Service not found'))
            return redirect(services)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(registrarLogin)


@login_required(login_url='registrar_login')
def citizenList(request):
    if request.user.is_authenticated and request.user.is_registrar == True:
        if 'new_citizen' in request.POST:
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            nationality = request.POST.get("nationality")
            nid_number = request.POST.get("nid_number")
            birthdate = request.POST.get("birthdate")
            birth_place = request.POST.get("birth_place")
            gender = request.POST.get("gender")
            marital_status = request.POST.get("marital_status")

            if first_name and last_name and nationality and birthdate and birth_place and gender and marital_status:
                if Citizen.objects.filter(nid_number=nid_number).exists():
                    messages.warning(request, "The citizen with " +
                                     nid_number+", Already exist.")
                    return redirect(citizenList)
                else:
                    # add new citizen
                    add_citizen = Citizen(
                        first_name=first_name,
                        last_name=last_name,
                        nationality=nationality,
                        nid_number=nid_number,
                        birthdate=birthdate,
                        birth_place=birth_place,
                        gender=gender,
                        marital_status=marital_status,
                    )
                    add_citizen.save()

                    messages.success(
                        request, "Citizen registered successfully.")
                    return redirect(citizenList)
            else:
                messages.error(request, ('All fields are required.'))
                return redirect(citizenList)
        else:
            newApplications = DocumentApplication.objects.filter(
                status__isnull=True)
            # getting citizens
            CitizenData = Citizen.objects.filter()
            context = {
                'title': 'Registrar - Citizen List',
                'citizenList_active': 'active',
                'citizens': CitizenData,
                'newApplications': newApplications,
            }
            return render(request, 'management/registrar/citizen_list.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(registrarLogin)


@login_required(login_url='registrar_login')
def citizenEdit(request, pk):
    if request.user.is_authenticated and request.user.is_registrar == True:
        citizen_id = pk
        # getting citizen
        if Citizen.objects.filter(id=citizen_id).exists():
            # if exists
            citizenData = Citizen.objects.get(id=citizen_id)
            # get parent data
            parentData = CitizenParent.objects.filter(citizen=citizen_id)
            # get document data
            documentData = CitizenDocument.objects.filter(citizen=citizen_id)

            if 'update_citizen' in request.POST:
                # Retrieve the form data from the request
                first_name = request.POST.get("first_name")
                last_name = request.POST.get("last_name")
                nationality = request.POST.get("nationality")
                nid_number = request.POST.get("nid_number")
                birthdate = request.POST.get("birthdate")
                birth_place = request.POST.get("birth_place")
                gender = request.POST.get("gender")
                marital_status = request.POST.get("marital_status")

                if first_name and last_name and nationality and birthdate and birth_place and gender and marital_status:

                    if Citizen.objects.filter(nid_number=nid_number).exclude(id=citizen_id).exists():
                        messages.warning(request, "The citizen with " +
                                         nid_number+", Already exist.")
                        return redirect(citizenEdit, pk)
                    else:
                        # Update Service
                        citizen_updated = Citizen.objects.filter(id=citizen_id).update(
                            first_name=first_name,
                            last_name=last_name,
                            nationality=nationality,
                            nid_number=nid_number,
                            birthdate=birthdate,
                            birth_place=birth_place,
                            gender=gender,
                            marital_status=marital_status,
                        )
                        if citizen_updated:
                            messages.success(
                                request, "Citizen profile updated successfully.")
                            return redirect(citizenEdit, pk)
                        else:
                            messages.error(request, ('Process Failed.'))
                            return redirect(citizenEdit, pk)
                else:
                    messages.error(request, ('All fields are required.'))
                    return redirect(citizenEdit, pk)

            elif 'update_address' in request.POST:
                # Retrieve the form data from the request
                province = request.POST.get("province")
                state = request.POST.get("state")
                city = request.POST.get("city")
                street = request.POST.get("street")

                if province and state and city and street:
                    # Update address
                    address_updated = CitizenAddress.objects.filter(citizen=citizen_id).update(
                        province=province,
                        state=state,
                        city=city,
                        street=street
                    )
                    if address_updated:
                        messages.success(
                            request, "Citizen address updated successfully.")
                        return redirect(citizenEdit, pk)
                    else:
                        messages.error(request, ('Process Failed.'))
                        return redirect(citizenEdit, pk)
                else:
                    messages.error(request, ('All fields are required.'))
                    return redirect(citizenEdit, pk)

            elif 'update_parents' in request.POST:
                father_fname = request.POST.get("father_fname")
                father_lname = request.POST.get("father_lname")
                father_profession = request.POST.get("father_profession")
                mother_fname = request.POST.get("mother_fname")
                mother_lname = request.POST.get("mother_lname")
                mother_profession = request.POST.get("mother_profession")

                if father_fname and father_lname and father_profession and mother_fname and mother_lname and mother_profession:
                    # Update address
                    parentF_updated = CitizenParent.objects.filter(citizen=citizen_id, parent="Father").update(
                        first_name=father_fname,
                        last_name=father_lname,
                        professionalism=father_profession
                    )
                    parentM_updated = CitizenParent.objects.filter(citizen=citizen_id, parent="Mother").update(
                        first_name=mother_fname,
                        last_name=mother_lname,
                        professionalism=mother_profession
                    )
                    if parentF_updated and parentM_updated:
                        messages.success(
                            request, "Citizen parent info updated successfully.")
                        return redirect(citizenEdit, pk)
                    else:
                        messages.error(request, ('Process Failed.'))
                        return redirect(citizenEdit, pk)
                else:
                    messages.error(request, ('All fields are required.'))
                    return redirect(citizenEdit, pk)

            elif 'delete' in request.POST:
                # Delete Citizen
                delete_citizen = Citizen.objects.get(id=citizen_id)
                delete_citizen.delete()
                messages.success(request, "Citizen info deleted successfully.")
                return redirect(citizenList)

            else:
                newApplications = DocumentApplication.objects.filter(
                    status__isnull=True)
                context = {
                    'title': 'Registrar - Citizen Info',
                    'citizenList_active': 'active',
                    'citizen': citizenData,
                    'parents': parentData,
                    'documents': documentData,
                    'newApplications': newApplications,
                }
                return render(request, 'management/registrar/citizen_info.html', context)
        else:
            messages.error(request, ('Citizen not found'))
            return redirect(citizenList)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(registrarLogin)
