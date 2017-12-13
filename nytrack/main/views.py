from django.shortcuts import render
from .forms import PassengerForm, SearchTrainForm
from .models import Segment, Station, SeatsFree, StopsAt
from datetime import date, datetime, time, timedelta


def search(request):
    context = {}
    form1 = SearchTrainForm(request.POST or None)

    if request.method == 'POST':
        print request.POST

        if form1.is_valid():
            context = searchAvailableTrain(request.POST)

            if len(context) > 1:
                return render(request, 'main/result.html', context)
            else:
                return render(request, 'main/error.html', context)
    else:
        context = {
            'form1': form1,
        }
    return render(request, 'main/search.html', context)


def searchAvailableTrain(request_POST):
    context = {}

    tempChoiceStartStation = Station.objects.get(id=request_POST['start'])  # Specific start station object
    tempChoiceEndStation = Station.objects.get(id=request_POST['end'])  # Specific end station object

    if tempChoiceStartStation == tempChoiceEndStation:
        context['title'] = "Please choose a different starting or ending station, Thank you"
        return context

    if tempChoiceStartStation.id < tempChoiceEndStation.id:  # Trip Heading North

        tripSegmentStart = Segment.objects.get(seg_south_end=tempChoiceStartStation)
        tempChoiceDate = request_POST['date']  # Selected date
        seatsFreeObject = SeatsFree.objects.filter(sf_segment=tripSegmentStart, sf_date=tempChoiceDate)

        if not seatsFreeObject:
            context['title'] = "There are no available trains at this given time. Please choose different time"
            return context

        startingPoint = seatsFreeObject[0]
        cursorPoint = startingPoint

        if startingPoint.sf_count == 0:
            message = "Every Ticket is booked at" + str(tempChoiceStartStation) + "at this time" + str(
                cursorPoint.sf_date)
            context['title'] = message
            return context

        tripSegmentEnd = Segment.objects.get(seg_north_end=tempChoiceEndStation)

        path_train = startingPoint.sf_train
        trip_date = datetime.strptime(tempChoiceDate, '%Y-%m-%d %H:%M:%S')

        all_seats_free = SeatsFree.objects.all()
        all_stops_at = StopsAt.objects.all()

        print "TRIP DATE START: ", trip_date
        while cursorPoint.sf_segment.id != tripSegmentEnd.id:
            tempSegment = Segment.objects.get(seg_south_end=cursorPoint.sf_segment.seg_north_end)
            print "SEGMENTS ALONG THE PATH: ", tempSegment

            tmp_stop = all_stops_at.get(sa_train=path_train, sa_station=tempSegment.seg_south_end)  # NEW CODE
            print "STOPSAT INSTANCE to get time_in of that train at that stop:", tmp_stop

            trip_date = datetime.combine(trip_date.date(), tmp_stop.sa_time_in)
            print "SEGMENT:", tempSegment, "LOOK UP TRIP DATE IN SEATSFREE: ", trip_date

            row = all_seats_free.get(sf_segment=tempSegment, sf_train=path_train, sf_date=trip_date)  # NEW CODE

            if row.sf_count == 0:
                context['title'] = "Train Booked from this destination please choose a different time"
                return context

            cursorPoint = row
            trip_date = cursorPoint.sf_date
            print "NEW DATE: ", trip_date

        arrive_time = StopsAt.objects.get(sa_train=startingPoint.sf_train, sa_station=tempChoiceEndStation)

        context = {
            'title': "Train available - Book before its too late !",
            'start_station': str(tempChoiceStartStation.station_name),
            'depart_date': str(tempChoiceDate),
            'end_station': str(tempChoiceEndStation.station_name),
            'arrive_date': str(arrive_time.sa_time_in),
            'train_number': str(startingPoint.sf_train),
        }

        return context

    else:
        tripSegmentStart = Segment.objects.get(seg_north_end=tempChoiceStartStation)
        tempChoiceDate = request_POST['date']  # Selected date
        seatsFreeObject = SeatsFree.objects.get(sf_segment=tripSegmentStart, sf_date=tempChoiceDate)

        if not seatsFreeObject:
            context['title'] = "There are no available trains at this given time. Please choose different time"
            return context

        startingPoint = seatsFreeObject
        cursorPoint = startingPoint

        if startingPoint.sf_count == 0:
            message = "Every Ticket is booked at" + str(tempChoiceStartStation) + "at this time" + str(cursorPoint.sf_date)
            context['title'] = message
            return context

        tripSegmentEnd = Segment.objects.get(seg_south_end=tempChoiceEndStation)

        path_train = startingPoint.sf_train  # NEW CODE
        trip_date = datetime.strptime(tempChoiceDate, '%Y-%m-%d %H:%M:%S')

        all_seats_free = SeatsFree.objects.all()  # get all of the entries so that its cached
        all_stops_at = StopsAt.objects.all()

        while cursorPoint.sf_segment.id != tripSegmentEnd.id:
            tempSegment = Segment.objects.get(seg_north_end=cursorPoint.sf_segment.seg_south_end)

            tmp_stop = all_stops_at.get(sa_train=path_train, sa_station=tempSegment.seg_north_end)  # NEW CODE

            trip_date = datetime.combine(trip_date.date(), tmp_stop.sa_time_in)
            print "SEGMENT:", tempSegment, "LOOK UP TRIP DATE IN SEATSFREE: ", trip_date

            row = all_seats_free.get(sf_segment=tempSegment, sf_train=path_train, sf_date=trip_date)  # NEW CODE

            if row.sf_count == 0:
                context['title'] = "Train Booked from this destination please choose a different time"
                return context

            cursorPoint = row
            trip_date = cursorPoint.sf_date
            print "NEW DATE: ", trip_date

        arrive_time = StopsAt.objects.get(sa_train=startingPoint.sf_train, sa_station=tempChoiceEndStation)

        context = {
            'title': "Train available - Book before its too late !",
            'start_station': str(tempChoiceStartStation.station_name),
            'depart_date': str(tempChoiceDate),
            'end_station': str(tempChoiceEndStation.station_name),
            'arrive_date': str(arrive_time.sa_time_in),
            'train_number': str(startingPoint.sf_train),
        }

        return context
