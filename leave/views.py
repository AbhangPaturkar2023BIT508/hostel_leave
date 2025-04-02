from django.shortcuts import render, redirect
from .models import HostelUser, LeaveApplication
from .forms import HostelUserForm
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect
from django.contrib.auth import logout

from django.shortcuts import get_object_or_404, redirect
from .models import LeaveApplication

def approve_leave(request, leave_id):
    # Get the leave application by ID
    leave_application = get_object_or_404(LeaveApplication, id=leave_id)
    leave_application.status = 'approved'  # Update the status
    leave_application.save()

    # Redirect back to the rector dashboard
    return redirect('rector_dashboard') 

def reject_leave(request, leave_id):
    # Get the leave application by ID
    leave_application = get_object_or_404(LeaveApplication, id=leave_id)
    leave_application.status = 'rejected'  # Update the status
    leave_application.save()

    # Redirect back to the rector dashboard
    return redirect('rector_dashboard') 

def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('login')  # Redirect to login page after logout

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = HostelUser.objects.get(username=username)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                if user.role == 'student':
                    return redirect('student_dashboard')
                else:
                    return redirect('rector_dashboard')
            else:
                return render(request, 'login.html', {'error': 'Invalid username or password.'})
        except HostelUser.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})

    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        form = HostelUserForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user with hashed password
            return redirect('login')
    else:
        form = HostelUserForm()
    return render(request, 'register.html', {'form': form})

def student_dashboard(request):
    # Fetch the student based on the user ID from the session
    student = HostelUser.objects.get(id=request.session['user_id'])
    
    # Get leave applications that belong to the student with status 'Pending' or 'Approved'
    leave_applications = LeaveApplication.objects.filter(student=student, status__in=['pending', 'approved'])
    
    # Pass the filtered leave applications to the template for rendering
    return render(request, 'student_dashboard.html', {'leave_applications': leave_applications})





def rector_dashboard(request):
    leave_applications = LeaveApplication.objects.filter(status='pending')
    return render(request, 'rector_dashboard.html', {'leave_applications': leave_applications})


from django.shortcuts import render, redirect
from .models import LeaveApplication, HostelUser  # Assuming your models are imported

def apply_leave(request):
    
    if not request.session.get('user_id'):
        return redirect('login')  # If user is not logged in, redirect to login

    student = HostelUser.objects.get(id=request.session['user_id'])

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')  # Get the reason field

        # Ensure valid date range and reason
        if start_date and end_date and reason:
            leave_application = LeaveApplication.objects.create(
                student=student,
                start_date=start_date,
                end_date=end_date,
                reason=reason  # Save the reason along with the dates
            )
            leave_application.save()
            return redirect('student_dashboard')  # Redirect after saving
        else:
            return render(request, 'student_dashboard.html', {'error': 'Please fill in all fields with valid values.'})


    return render(request, 'student_dashboard.html')
