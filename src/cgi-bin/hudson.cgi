#!/bin/sh



exec "$COMMANDER_HOME/bin/ec-perl" -x "$0" "${@}"



#!perl



use CGI;

use LWP::UserAgent;

use XML::XPath;



my $data;

read(STDIN, $data, $ENV{'CONTENT_LENGTH'}); 

my $args = new XML::XPath($data);



my $uri = $ENV{'SCRIPT_URI'};

$uri =~ s{/plugins/.*}{};



print "Content-type: text/html\n\n";



print '<table class="data" id="jobsQuickView_table0" cellspacing="0">

  <tbody>';



my $count = 0;

my %procSeen = {};

my %procCount = {};

my %procSuccess = {};



map {

    my $jobName = $_->findvalue("jobName");

    my $procName = $_->findvalue("procedureName");

    my $projName = $_->findvalue("projectName");

    my $outcome = $_->findvalue("outcome");



    my $procIndex = $procName." ".$projName;

    $procCount{$procIndex}++;

    if ($outcome eq "success")

    {

      $procSuccess{$procIndex}++;

    }

} ($args->findnodes("//object/job"));



print qq(

<tr align="left">

  <th>

    Status

  </th>

  <th>

    Weather

  </th>

  <th>

    Procedure Name

  </th>

  <th>

    Project Name

  </th>

  <th>

    Most Recent Job

  </th>

  <th>

    Jobs

  </th>

  <th>

    Successes

  </th>

  <th>

    Time

  </th>

</tr>);





map {

    my $jobName = $_->findvalue("jobName");

    my $procName = $_->findvalue("procedureName");

    my $projName = $_->findvalue("projectName");

    my $outcome = $_->findvalue("outcome");

    my $status = $_->findvalue("status");

    my $jobId = $_->findvalue("jobId");

    my $time = $_->findvalue('elapsedTime')->value();



    my $class = ($count = !$count) ? 'oddRow' : 'blankRow';

    my $time = sprintf("%02d:%02d:%02d.%03d",

                       $time / 3600000,

                       ($time / 60000) % 60,

                       ($time / 1000) % 60,

                       $time % 1000);



    my $procIndex = $procName." ".$projName;

    my $rating = $procSuccess{$procIndex} / $procCount{$procIndex};

    my $iconChoice = "<img src=/commander/plugins/HudsonDashboard-1.0/images/health-00to19.gif width=24 height=24>";

    if ($rating >= 0.8)

    {

	$iconChoice = "<img src=/commander/plugins/HudsonDashboard-1.0/images/health-80plus.gif width=24 height=24>";

    }

    elsif ($rating >= 0.6)

    {

	$iconChoice = "<img src=/commander/plugins/HudsonDashboard-1.0/images/health-60to79.gif width=24 height=24>";

    }

    elsif ($rating >= 0.4)

    {

	$iconChoice = "<img src=/commander/plugins/HudsonDashboard-1.0/images/health-40to59.gif width=24 height=24>";

    }

    elsif ($rating >= 0.2)

    {

	$iconChoice = "<img src=/commander/plugins/HudsonDashboard-1.0/images/health-20to39.gif width=24 height=24>";

    }

    if ($procSuccess{$procIndex} == "")

    {

	    $procSuccess{$procIndex} = 0;

    }



    my $imageName = "blue";

    if ($outcome eq "error")

    {

    	$imageName = "red";

    }

    elsif ($outcome eq "warning")

    {

    	$imageName = "yellow";

    }

    if ("$status" ne "completed")

    {

      $imageName = $imageName."_anime";

    }

    my $imageChoice = "<img src=/commander/plugins/HudsonDashboard-1.0/images/$imageName.gif width=24 height=24>";

    

    print qq(

<tr class="$class">

  <td>

    $imageChoice

  </td>

  <td>

    $iconChoice

  </td>

  <td>

    <a href="$uri/link/procedureDetails/projects/$projName/procedures/$procName">$procName</a>

  </td>

  <td>

    <a href="$uri/link/projectDetails/projects/$projName">$projName</a>

  </td>

  <td>

    <a href="$uri/link/jobDetails/jobs/$jobId">$jobName</a>

  </td>

  <td>

    $procCount{$procIndex}

  </td>

  <td>

    $procSuccess{$procIndex}

  </td>

  <td class="jobsQuickView_timeColumn">$time</td>

</tr>) unless $procSeen{$procIndex};



    $procSeen{$procIndex} = 1;

} ($args->findnodes("//object/job"));



print '</tbody></table>';