from __future__ import unicode_literals
from django.db import models
from django.core.validators import MaxValueValidator

# Django automatically creates an auto increment primary key for every table

class Station(models.Model):
    station_name = models.CharField(unique=True, max_length=50, verbose_name='Station Name', null=False)
    station_symbol = models.CharField(unique=True, max_length=5, verbose_name='Station Symbol')

    def __unicode__(self):
        return unicode(self.station_name)

class Train(models.Model):
    train_number = models.CharField(null=False, max_length=15, verbose_name='Train Number')

    start_station = models.ForeignKey(Station, related_name='s_start', verbose_name='Start Station')
    end_station = models.ForeignKey(Station, related_name='s_end', verbose_name='End Station')
    train_direction = models.BooleanField(help_text='North = 1, South = 0', verbose_name='Direction')
    train_days = models.CharField(max_length=20, verbose_name='Days train runs', help_text='M-T-W-Th-F-S-Su')

    def __unicode__(self):
        return unicode(self.train_number)

class Passenger(models.Model):
    p_f_name = models.CharField(max_length=15, verbose_name='First Name')
    p_l_name = models.CharField(max_length=15, verbose_name='Last Name')
    billing_address = models.CharField(max_length=50, verbose_name='Billing Address')
    email = models.EmailField(default=0)

    def __unicode__(self):
        return self.p_f_name

class Segment(models.Model):
    seg_north_end = models.ForeignKey(Station, related_name='n_end+', verbose_name='Segment North End')
    seg_south_end = models.ForeignKey(Station, related_name='s_end+', verbose_name='Segment South End')
    seg_fare = models.IntegerField(verbose_name='Fare', null=False)
    seg_distance = models.IntegerField(default=0, verbose_name='Mileage Between Stations', null=False)

    def __unicode__(self):
        return unicode(self.seg_north_end)

class SeatsFree(models.Model):
    sf_segment = models.ForeignKey(Segment, related_name='seg+', verbose_name='Segment',
                                   help_text='Shows only north-end station of segment')
    sf_train = models.ForeignKey(Train, related_name='sf_train+', verbose_name='Train in Segment')
    sf_date = models.DateTimeField(verbose_name='Date', help_text='All reservations start June 1st 2017, 6:00am')
    sf_count = models.PositiveIntegerField(validators=[MaxValueValidator(448)], verbose_name='Free Seats in Segment',
                                           help_text='0 <= n <= 448')

    def __unicode__(self):
        return unicode(self.sf_segment)

class PaymentMethod(models.Model):
    type = models.CharField(max_length=10, verbose_name='Type of payment')

    def __unicode__(self):
        return self.type

class TicketTrip(models.Model):
    trip_start_station = models.ForeignKey(Station, related_name='t_start+', verbose_name='Trip Start Station')
    trip_end_station = models.ForeignKey(Station, related_name='t_end+', verbose_name='Trip End Station')

    trip_train = models.ForeignKey(Train, verbose_name='Train', blank=True, null=True)

    trip_fare = models.IntegerField(default=0, verbose_name='Fare')

    trip_pay_method = models.ForeignKey(PaymentMethod, related_name='t_pay', verbose_name='Choose Payment')
    trip_date = models.DateTimeField(verbose_name='Trip Date')

    trip_segment_start = models.ForeignKey(Segment, related_name='s_start+', verbose_name='Segment Start',
                                           help_text='Shows only north-end station of segment', blank=True, null=True)
    trip_segment_end = models.ForeignKey(Segment, related_name='s_end+', verbose_name='Segment End',
                                         help_text='Shows only north-end station of segment', blank=True, null=True)

    def __unicode__(self):
        return unicode(self.trip_start_station)

class StopsAt(models.Model):
    sa_train = models.ForeignKey(Train, related_name='train+', verbose_name='Which Train?')
    sa_station = models.ForeignKey(Station, null=True, related_name='station+', verbose_name='Station Where Train Stops')
    sa_time_in = models.TimeField(verbose_name='Time-In of Train at Station')
    sa_time_out = models.TimeField(verbose_name='Time-out of train at Station', null=True, blank=True)

    def __unicode__(self):
        return unicode(self.sa_train)
