from django.db import models

#Each class is a data model, which a table is created from
class Voter(models.Model):
    employment = models.CharField('Employment Status', max_length=1)
    age_band = models.CharField('Age Band', max_length=1)
    country = models.CharField('Country', max_length=30)
    local_area = models.CharField('Local Area', max_length=30)
    gender = models.CharField('Gender', max_length=1)
    last_login = models.DateTimeField('Last Login Time')
    employment_dict = {"P" : "Part-time", "F" : "Full-time", "S" : "Student", "U" : "Unemployed", "N" : "Prefer not to say"}
    age_band_dict = {"A" : "Under 18", "B" : "18-30", "C" : "31-50", "D" : "51-65", "E" : "Over 65", "F" : "Prefer not to say"}
    gender_dict = {"M" : "Male", "F" : "Female", "O" : "Other", "P" : "Prefer not to say"}


class Poll(models.Model):
    vote_area = models.CharField('Voters Must Be From', max_length=20)
    start_time = models.DateTimeField('Start Time')
    end_time = models.DateTimeField('End Time')
    poll_type = models.CharField('Poll Type', max_length=6)
    title = models.CharField('Poll Title', max_length=40)
    question = models.CharField('Poll Question', max_length=240)
    values = models.CharField('Poll Answers', max_length=300)
    approved = models.BooleanField('Approved', default=False)

    def val_list(self):
        return self.values.split(';')
	
class Vote(models.Model):
    poll_id = models.ForeignKey(Poll, on_delete=models.CASCADE)
    voter_id = models.ForeignKey(Voter, on_delete=models.CASCADE)
    value = models.CharField('Choice', max_length=100)