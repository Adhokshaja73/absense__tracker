import datetime
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
# Create your models here.

# model for user role. User role can be either team_leader or team_member. user foreign key is used to link the user to the role
class UserRole(models.Model):
    USER_ROLE_CHOICES = ( (0, 'Team Leader'), (1, 'Team Member') )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.IntegerField(choices=USER_ROLE_CHOICES, default=2)

    def __str__(self):
        return self.user.username + ' - ' + self.USER_ROLE_CHOICES[self.role][1]


#  userprofile Model that stores user info like phone number, address, email and user foreign key is used to link the user to the profile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=100, blank=True)
    profilePicture = models.ImageField(upload_to='profile_pictures', blank=True)

    email = models.EmailField(blank=True)
    def __str__(self):
        return self.user.username + ' - ' + self.email
    
# model for team. team_leader foreign key is used to link the team leader to the team
# team_members is a many to many field that links the team members to the team
class Team(models.Model):
    team_leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_leader')
    team_members = models.ManyToManyField(User, related_name='team_members')
    team_name = models.CharField(max_length=50, blank=True)
    def __str__(self):
        return self.team_name

    # clean method to validate the team leader and team members
    def clean(self):
        # check if team leader is in team members
        leaderRole = UserRole.objects.filter(user = self.team_leader)
        if(not leaderRole.exists() or leaderRole.get().role != 0):
            ValidationError("Selected team leader is not of role Team Lead")  
    
    
# model for leave application. user foreign key is used to link the user who applied for leave to the leave application
# team foreign key is used to link the team to the leave application
# reason is a text field that stores the reason for leave
# start_date and end_date are date fields that store the start and end date of leave
# status is a choice field that stores the status of the leave application
class LeaveApplication(models.Model):
    LEAVE_STATUS_CHOICES = ( (1, 'Pending'), (2, 'Approved'), (3, 'Rejected') )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    reason = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.IntegerField(choices=LEAVE_STATUS_CHOICES, default=1)
    applied_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username + ' - ' + self.team.team_name + ' - ' + self.reason

    # clean method to validate the leave application
    def clean(self):
        # check if start date is before end date
        if self.start_date > self.end_date:
            raise ValidationError('Start date cannot be after end date')
        # # check if leave application is for the same team
        # if self.team not in self.user.team_members.all():
        #     raise ValidationError('Leave application is not for the same team')
        
# notification model that stores the notification message and the user to whom the notification is sent
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    message = models.TextField()

    def __str__(self):
        return self.user.username + ' - ' + self.message




class CalenderEvent(models.Model):
    title = models.CharField(max_length=100)
    startDateTime = models.DateTimeField()
    endDateTime = models.DateTimeField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)


class Ticket_type(models.Model):
    ticket_type_name = models.CharField(max_length=30, verbose_name="Ticket-type name")
    ticket_type_desc = models.TextField(verbose_name="Description")
    ticket_type_active = models.BooleanField(default=True)

    def __str__(self):
        return self.ticket_type_name

class TeamTicket(models.Model):
    STATUS_CHOICES = ((0,'raised'), (1,'processing'), (2,'rejected'), (3,'closed'), (4,'Deleted'))

    ticket_number = models.CharField(max_length=10,null=True, blank=True,verbose_name="Ticket number")

    ticket_type = models.ForeignKey(Ticket_type,on_delete=models.CASCADE, related_name='ticket_type' , verbose_name="Ticket type")
    raised_date = models.DateTimeField(auto_now_add=True, verbose_name="Raised Date")
    raised_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ticket_user')
    issue_detail = models.TextField(verbose_name="Issue Details")
    issue_date = models.DateTimeField(auto_now_add=False,null=True, blank=True, verbose_name="Issue date")

    response_date = models.DateTimeField(auto_now_add=False,null=True, blank=True, verbose_name="Response date")
    response_by = models.ForeignKey( User,on_delete=models.CASCADE,null=True, blank=True,verbose_name="Response by")
    comments = models.TextField(null=True, blank=True,verbose_name="comments by Teamlead")

    ticket_status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    closed_date = models.DateTimeField(auto_now_add=False,null=True, blank=True, verbose_name="Closed date")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='teamfk')
    closed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='close_ticket_user',null=True, blank=True,verbose_name="Closed by")

    def __str__(self):
        return self.ticket_number
    