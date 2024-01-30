from django.db import models

class Employee(models.Model):
    ID = models.AutoField(primary_key=True)
    First_Name = models.CharField(max_length=50)
    Last_Name = models.CharField(max_length=50)
    Address = models.CharField(max_length=255)
    Phone_Number = models.CharField(max_length=15)
    Email_Address = models.EmailField(max_length=100)
    Joining_Date = models.DateField()
    Job_Level = models.CharField(max_length=50)
    Is_Remote_Employee = models.BooleanField()
    Job_Description = models.CharField(max_length=100)
    Designation = models.CharField(max_length=50)

    def __str__(self):
        return self.First_Name + " " + self.Last_Name

class Skill(models.Model):
    ID = models.AutoField(primary_key=True)
    Skill_Name = models.CharField(max_length=50)
    Skill_Proficiency = models.CharField(max_length=50)

    def __str__(self):
        return self.Skill_Name

class Emp_Skill(models.Model):
    ID = models.AutoField(primary_key=True)
    Employee_ID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    Skill_ID = models.ForeignKey(Skill, on_delete=models.CASCADE)

class Project(models.Model):
    ID = models.AutoField(primary_key=True)
    Project_Name = models.CharField(max_length=100)
    Is_Live = models.BooleanField()
    Description = models.CharField(max_length=255)

    def __str__(self):
        return self.Project_Name

class Emp_Project(models.Model):
    ID = models.AutoField(primary_key=True)
    Employee_ID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    Project_ID = models.ForeignKey(Project, on_delete=models.CASCADE)
    Role = models.CharField(max_length=50)

class Chat_History(models.Model):
    ID = models.AutoField(primary_key=True)
    Employee_ID = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    Message = models.TextField()
    Response = models.TextField()
    Timestamp = models.DateTimeField(auto_now_add=True)
