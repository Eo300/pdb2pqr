#!@WHICHPYTHON@
"""
  CGI Module for checking on the status of an OPAL job
"""

__date__   = "4 January 2010"
__author__ = "Wes Goodman, Samir Unni, Yong Huang"

import sys
import cgi
import cgitb
import os,shutil,glob,string,time,urllib
from src.server import *
from src.aconf import *
from src.utilities import getTrackingScriptString, getEventTrackingString

cgitb.enable()
form = cgi.FieldStorage()

def printheader(pagetitle,refresh=None,jobid=None):
    str = ""
    str+= "<html>\n"
    str+= "<HEAD>\n"
    str+= '<img src="https://raw.githubusercontent.com/Electrostatics/apbs-pdb2pqr/master/apbs/doc/icons/APBS_128_v2.png" style="float:right; position:relative;right:200px; top: 2px;">'
    if refresh:
        str+= "\t<META HTTP-EQUIV=\"Refresh\" CONTENT=\"%s\">\n" % refresh
    str+= "\t<TITLE>%s</TITLE>\n" % pagetitle
    str+= "\t<link rel=\"stylesheet\" href=\"%s\" type=\"text/css\">\n" % STYLESHEET
    str+= getTrackingScriptString(jobid)
    str+= "</HEAD>\n"
    return str


#def getloads():
#    """
#        get the system load information for output and logging
#
#        returns
#            loads:  a three entry list containing the 1, 5, and
#                    15 minute loads. if the load file is not found,
#                    return none.
#    """
#    if loadpath == "": return none
#    try:
#        file = open(loadpath, 'ru')
#    except ioerror:
#        return none
#
#    line = file.readline()
#    words = string.split(line)
#    loads = words[:3]
#    
#    return loads

#def cleantmpdir():
#    """
#        clean up the temp directory for cgi.  if the size of the directory
#        is greater than limit, delete the older half of the files.  since
#        the files are stored by system time of creation, this is an
#        easier task.
#    """
#    newdir = []
#    size = 0.0
#    count = 0
#    path = INSTALLDIR + tmpdir
#
#    dir = os.listdir(path)
#    for filename in dir:
#        size = size + os.path.getsize("%s%s" % (path, filename))
#        period = string.find(filename,".")
#        id = filename[:period]
#        if id not in newdir:
#            newdir.append(id)
#            count += 1
#        
#    newdir.sort()
#    size = size / (1024.0 * 1024.0)
#    
#    newcount = 0
#    if size >= limit:
#        for filename in newdir:
#            if newcount > count/2.0: break
#            try:
#                os.remove("%s%s.pqr" % (path, filename))
#            except oserror: pass
#            try:
#                os.remove("%s%s.in" % (path, filename))
#            except oserror: pass
#            try:
#                os.remove("%s%s.html" % (path, filename))
#            except oserror: pass
#            newcount += 1
#
#def getquote(path):
#    """
#        get a quote to display for the refresh page.
#        uses fortune to generate a quote.
#
#        parameters:
#            path:   the path to the fortune script (str)
#        returns:
#            quote:   the quote to display (str)
#    """
#    fortune = os.popen(path)
#    quote = fortune.read()
#    quote = string.replace(quote, "\n", "<br>")
#    quote = string.replace(quote, "\t", "&nbsp;"*5)
#    quote = "%s<p>" % quote
#    return quote
#
#def printprogress(name, refreshname, reftime, starttime):
#    """
#        print the progress of the server
#
#        parameters
#            name:        the id of the html page to write to (string)
#            refreshname: the name of the html page to refresh to (string)
#            reftime:     the length of time to set the refresh wait to (int)
#            starttime:   the time as returned by time.time() that the run started (float)
#    """
#    elapsedtime = time.time() - starttime + refreshtime/2.0 # add in time offset
#    filename = "%s%s%s/%s-tmp.html" % (INSTALLDIR, tmpdir, jobid, name)
#    file = open(filename,"w")
#    file.write("<html>\n")
#    file.write("<head>\n")
#    file.write("<title>pdb2pqr progress</title>\n")
#    file.write("<link rel=\"stylesheet\" href=\"%s\" type=\"text/css\">\n" % stylesheet)
#    file.write("<meta http-equiv=\"refresh\" content=\"%s; url=%s\">\n" % \
#               (reftime, refreshname))
#    file.write("</head>\n")
#    file.write("<body>\n")
#    file.write("<h2>pdb2pqr progress</h2><p>\n")
#    file.write("the pdb2pqr server is generating your results - this page will automatically \n")
#    file.write("refresh every %s seconds.<p>\n" % refreshtime)
#    file.write("thank you for your patience!<p>\n")
#    file.write("server progress:<p>\n")
#    file.write("<blockquote>\n")
#    file.write("<font size=2>elapsed time:</font> <code>%.2f seconds</code><br>\n" % elapsedtime)
#    file.write("</blockquote>\n")
#    file.write("server information:<p>\n")
#    file.write("<blockquote>\n")
#    loads = getloads()
#    if loads != none:
#        file.write("<font size=2>server load:</font> <code>%s (1min)  %s (5min)  %s (15min)</code><br>\n" % (loads[0], loads[1], loads[2]))
#
#    file.write("<font size=2>server time:</font> <code>%s</code><br>\n" % (time.asctime(time.localtime())))
#    file.write("</blockquote>\n")
#    file.write("<script type=\"text/javascript\">")
#    file.write("var gaJsHost = ((\"https:\" == document.location.protocol) ? \"https://ssl.\" : \"http://www.\");")
#    file.write("document.write(unescape(\"%3Cscript src=\'\" + gaJsHost + \"google-analytics.com/ga.js\' type=\'text/javascript\'%3E%3C/script%3E\"));")
#    file.write("</script>")
#    file.write("<script type=\"text/javascript\">")
#    file.write("try {")
#    file.write("var pageTracker = _gat._getTracker(\"UA-11026338-3\");")
#    file.write("pageTracker._trackPageview();")
#    file.write("} catch(err) {}</script>")
#    file.write("</body></html>")
#    file.close()
#
#def createresults(header, input, name, time, missedligands=[]):
#    """
#        create the results web page for cgi-based runs
#
#        parameters
#            header: the header of the pqr file (string)
#            input:   a flag whether an input file has been created (int)
#            tmpdir:  the resulting file directory (string)
#            name:    the result file root name, based on local time (string)
#            time:    the time taken to run the script (float)
#            missedligands: a list of ligand names whose parameters could
#                     not be assigned. optional. (list)
#    """
#    newheader = string.replace(header, "\n", "<br>")
#    newheader = string.replace(newheader," ","&nbsp;")
#
#    filename = "%s%s%s/%s.html" % (INSTALLDIR, tmpdir, jobid, name)
#    file = open(filename, "w")
#    
#    file.write("<html>\n")
#    file.write("<head>\n")
#    file.write("<title>pdb2pqr results</title>\n")
#    file.write("<link rel=\"stylesheet\" href=\"%s\" type=\"text/css\">\n" % stylesheet)
#    file.write("</head>\n")
#
#    file.write("<body>\n")
#    file.write("<h2>pdb2pqr results</h2>\n")
#    file.write("<p>\n")
#    file.write("here are the results from pdb2pqr.  the files will be available on the ")
#    file.write("server for a short period of time if you need to re-access the results.<p>\n")
# 
#    file.write("<a href=\"%s%s%s.pqr\">%s.pqr</a><br>\n" % (website, tmpdir, name, name))
#    if input:
#        file.write("<a href=\"%s%s%s.in\">%s.in</a><br>\n" % (website, tmpdir, name, name))
#    pkaname = "%s%s%s/%s.propka" % (INSTALLDIR, tmpdir, jobid, name)
#    if os.path.isfile(pkaname):
#        file.write("<a href=\"%s%s%s.propka\">%s.propka</a><br>\n" % (website, tmpdir, name, name))
#    typename = "%s%s%s/%s-typemap.html" % (INSTALLDIR, tmpdir, jobid, name)
#    if os.path.isfile(typename):
#        file.write("<a href=\"%s%s%s-typemap.html\">%s-typemap.html</a><br>\n" % (website, tmpdir, name, name)) 
#    file.write("<p>the header for your pqr file, including any warnings generated, is:<p>\n")
#    file.write("<blockquote><code>\n")
#    file.write("%s<p>\n" % newheader)
#    file.write("</code></blockquote>\n")
#    if missedligands != []:
#        file.write("the forcefield that you have selected does not have ")
#        file.write("parameters for the following ligands in your pdb file.  please visit ")
#        file.write("<a href=\"http://davapc1.bioch.dundee.ac.uk/programs/prodrg/\">prodrg</a> ")
#        file.write("to convert these ligands into mol2 format.  this ligand can the be ")
#        file.write("parameterized in your pdb2pqr calculation using the peoe_pb methodology via ")
#        file.write("the 'assign charges to the ligand specified in a mol2 file' checkbox:<p>\n")
#        file.write("<blockquote><code>\n")
#        for item in missedligands:
#            file.write("%s<br>\n" % item)
#        file.write("<p></code></blockquote>\n")
#    file.write("if you would like to run pdb2pqr again, please click <a href=\"%s%s\">\n" % (website, webname))
#    file.write("here</a>.<p>\n")
#    file.write("if you would like to run apbs with these results, please click <a href=\"%s../apbs/index.py?pdb2pqr-id=%s\">here</a>.<p>\n" % (website[:-1], name))
#    file.write("<p>thank you for using the pdb2pqr server!<p>\n")
#    file.write("<font size=\"-1\"><p>total time on server: %.2f seconds</font><p>\n" % time)
#    file.write("<font size=\"-1\"><center><i>last updated %s</i></center></font>\n" % __date__) 
#    file.write("<script type=\"text/javascript\">")
#    file.write("var gaJsHost = ((\"https:\" == document.location.protocol) ? \"https://ssl.\" : \"http://www.\");")
#    file.write("document.write(unescape(\"%3Cscript src=\'\" + gaJsHost + \"google-analytics.com/ga.js\' type=\'text/javascript\'%3E%3C/script%3E\"));")
#    file.write("</script>")
#    file.write("<script type=\"text/javascript\">")
#    file.write("try {")
#    file.write("var pageTracker = _gat._getTracker(\"UA-11026338-3\");")
#    file.write("pageTracker._trackPageview();")
#    file.write("} catch(err) {}</script>")
#    file.write("</body>\n")
#    file.write("</html>\n")

def checkprogress(jobid=None,appServicePort=None,calctype=None):
    """
        Finds out if the job has been completed
    """
     
    if have_opal:
        
        # construct soap request
        try:
            status=appServicePort.queryStatus(queryStatusRequest(jobid))
        except Exception, e:
            return ["error"]
        if status._code == 4:
            return ["error"]

        if status._code == 8:
            return ["complete",status]
        else:
            return ["running",status]

    else:
        progress = []
        file = open('%s%s%s/%s_status' % (INSTALLDIR,TMPDIR,jobid, form["calctype"].value))

        for line in file.readlines():
            progress.append(string.strip(line))
        file.close()
        return progress

def mainCGI():
    """
        Main method for determining the query page output
    """
    logopts = {}
    print "Content-type: text/html\n\n"
    calctype = form["calctype"].value

    # prints version error, if it exists
    if form["jobid"].value == 'False':
        print printheader("%s Job Status Page" % calctype.upper())
        progress = "version_mismatch"
        runtime = 0
    elif form["jobid"].value == 'notenoughmem':
        print printheader("%s Job Status Page" % calctype.upper())
        progress = "not_enough_memory"
        runtime = 0
    else:
        progress = None
        
    #Check for error html
    errorpath = '%s%s%s.html' % (INSTALLDIR, TMPDIR, form["jobid"].value)
    if os.path.isfile(errorpath):
        string = ""
        string+= "<html>\n"
        string+= "\t<head>\n"
        string+= "\t\t<meta http-equiv=\"Refresh\" content=\"0; url=%s%s%s.html\">\n" % (WEBSITE, TMPDIR, form["jobid"].value)
        string+= "\t</head>\n"
        string+= "</html>\n"
        print string
        return

    # prepares for Opal query, if necessary
    if have_opal:
        if calctype=="pdb2pqr":
            opal_url = PDB2PQR_OPAL_URL
        elif calctype=="apbs":
            opal_url = APBS_OPAL_URL
        appLocator = AppServiceLocator()
        appServicePort = appLocator.getAppServicePort(opal_url)
    else:
        appServicePort = None

    # if PDB2PQR, determines if link to APBS calculation should be shown
    if calctype=="pdb2pqr":    
        #if(form["apbsinput"].value=="True"): # change to use a file
        #    apbs_input = True
        #else:
        #    apbs_input = False
        apbsInputFile = open('%s%s%s/apbs_input' % (INSTALLDIR, TMPDIR, form["jobid"].value))
        apbs_input = apbsInputFile.read()
        apbsInputFile.close()
        if apbs_input=="True":
            apbs_input = True
        else:
            apbs_input = False

        typemapInputFile = open('%s%s%s/typemap' % (INSTALLDIR, TMPDIR, form["jobid"].value))
        typemap = typemapInputFile.read()
        typemapInputFile.close()
        if typemap=="True":
            typemap = True
        else:
            typemap = False

    if have_opal and progress == None:
        if form["calctype"].value=="pdb2pqr":
            pdb2pqrJobIDFile = open('%s%s%s/pdb2pqr_opal_job_id' % (INSTALLDIR, TMPDIR, form["jobid"].value))
            jobid = pdb2pqrJobIDFile.read()
            pdb2pqrJobIDFile.close()
        elif form["calctype"].value=="apbs":
            apbsJobIDFile = open('%s%s%s/apbs_opal_job_id' % (INSTALLDIR, TMPDIR, form["jobid"].value))
            jobid = apbsJobIDFile.read()
            apbsJobIDFile.close()
    else:
        jobid = form["jobid"].value

    if progress == None:
        cp = checkprogress(jobid,appServicePort,calctype) # finds out status of job
        progress = cp[0]
    
    #initialize with bogus value just in case
    starttime = time.time()
    
    if progress == "running" or progress == "complete":
        timefile = open('%s%s%s/%s_start_time' % (INSTALLDIR, TMPDIR, form["jobid"].value, form["calctype"].value))
        starttime = float(timefile.read())
        timefile.close()
    if progress == "running" or (have_opal and progress not in ("version_mismatch", 
                                                                "not_enough_memory",
                                                                "error",
                                                                "complete")):
        runtime = time.time()-starttime
    elif progress == "complete":
        endTimeFileString = '%s%s%s/%s_end_time' % (INSTALLDIR, TMPDIR, form["jobid"].value, form["calctype"].value)
        if have_opal and not os.path.isfile(endTimeFileString):
            runtime = time.time()-starttime
            with open(endTimeFileString, 'w') as endTimeFile:
                endTimeFile.write(str(time.time()))
        else:
            with open(endTimeFileString, 'r') as endTimeFile:
                runtime = float(endTimeFile.read())-starttime
    else:
        runtime = -1
        
    if progress == "running":
        #if have_opal:
        #    resultsurl = cp[1]._baseURL
        #else:
        if calctype=="pdb2pqr":
            resultsurl = '%squerystatus.cgi?jobid=%s&apbsinput=%s&calctype=pdb2pqr' % (WEBSITE, form["jobid"].value, apbs_input)
        else:
            resultsurl = '%squerystatus.cgi?jobid=%s&calctype=apbs' % (WEBSITE, form["jobid"].value)

    if progress == "complete":
        print printheader("%s Job Status Page" % calctype.upper(), jobid=form["jobid"].value)

    elif progress == "error":
        print printheader("%s Job Status Page - Error" % calctype.upper(),0, jobid=form["jobid"].value)

    elif progress == "running": # job is not complete, refresh in 30 seconds
        print printheader("%s Job Status Page" % calctype.upper(), refresh, jobid=form["jobid"].value)

    print "<BODY>\n<P>"
    print "<p></p>"
    print '<div id="content">'
    print "<h3>Status:"
    if progress == "complete":
        color = "2CDE56" 
    elif progress == "running":
        color = "ffcc00"
    else:
        color = "FA3434"
#     color = "34A6E3" if progress == "complete"  
#     color = "ffcc00" if progress == "running"
#     color = "FA3434" if progress != "complete" or "running"
    if progress == "complete":
        image = "http://i61.tinypic.com/2w3yhhc.png" 
    elif progress == "running":
        image = "http://i61.tinypic.com/2ccpct2.png"
    else:
        image = "http://i57.tinypic.com/1zgxria.png"
    print "<strong style=\"color:#%s;\">%s</strong>" % (color, progress)
    print "<img src=\"%s\"><br />" % image
    print "</h3>"
    print "Run time: %s seconds<br />" % int(runtime)
    print "Current time: %s<br />" % time.asctime()
    print "</P>\n<HR>\n<P>"

    if progress == "complete":
        if calctype=="pdb2pqr":
            nexturl = 'apbs_cgi.cgi?jobid=%s' % form["jobid"].value
        else:
            nexturl = 'visualize.cgi?jobid=%s' % form["jobid"].value

        if have_opal:    
            resp = appServicePort.getOutputs(getOutputsRequest(jobid))
            filelist = resp._outputFile

        print "Here are the results:<ul>"
        print "<li>Input files<ul>"

        if calctype=="pdb2pqr":
            # this code should be cleaned up once local PDB2PQR runs output the PDB file with the .pdb extension
            if have_opal:
                for i in range(0,len(filelist)):
                    if len(filelist[i]._name) == 4:
                        print "<li><a href=%s>%s</a></li>" % (filelist[i]._url, filelist[i]._name)
            else:
                print "<li><a href=%s%s%s/%s.pdb>%s.pdb</a></li>" % (WEBSITE, TMPDIR, jobid, jobid, jobid)

        elif calctype=="apbs":
            if have_opal:
                for i in range(0,len(filelist)):
                    if filelist[i]._name == "apbsinput.in" or filelist[i]._name[-4:] == ".pqr":
                        print "<li><a href=%s>%s</a></li>" % (filelist[i]._url, filelist[i]._name)
            else:
                print "<li><a href=%s%s%s/apbsinput.in>apbsinput.in</a></li>" % (WEBSITE, TMPDIR, jobid)
                print "<li><a href=%s%s%s/%s.pqr>%s.pqr</a></li>" % (WEBSITE, TMPDIR, jobid, jobid, jobid)

        print "</ul></li>"
        print "<li>Output files<ul>"
        
        queryString = [str(os.environ["REMOTE_ADDR"])]
        # Getting PDB2PQR run log info
        if os.path.isfile('%s%s%s/pdb2pqr_log' % (INSTALLDIR, TMPDIR, jobid)):
            pdb2pqrLogFile=open('%s%s%s/pdb2pqr_log' % (INSTALLDIR, TMPDIR, jobid), 'r')
            logstr=pdb2pqrLogFile.read().split('\n')
            templogopts = eval(logstr[0])
            pdb2pqrLogFile.close()
            queryString.insert(0, templogopts.get('pdb',''))
        
        if calctype=="pdb2pqr":                            
            if have_opal:
                for i in range(0,len(filelist)):
                    if filelist[i]._name.endswith((".propka", "-typemap.html", ".pqr", ".in")):
#                        if filelist[i]._name[-4:]==".pqr":
#                            # Getting pqr file length for PDB2PQR Opal run
#                            f=urllib.urlopen(filelist[i]._url)
#                            #pqrOpalFileLength = len(f.readlines())
#                            f.close()
                        print "<li><a href=%s>%s</a></li>" % (filelist[i]._url, filelist[i]._name)
                        
                    #Get the first line of the summary file.
                    if filelist[i]._name.endswith(".summary"):
                        f=urllib.urlopen(filelist[i]._url)
                        summaryLine = f.readline().strip()
                        #logopts["pdb"]=logopts.get("pdb", "") + "|" + summaryLine
                        queryString.append(summaryLine)
                        f.close()
#                logRun(logopts, runtime, pqrOpalFileLength, logff, REMOTE_ADDR)
            else:
                #Get the first line of the summary file.
                summaryFile = '%s%s%s/%s%s' % (INSTALLDIR, TMPDIR, jobid, jobid, ".summary")
                if os.path.isfile(summaryFile):
                    with open(summaryFile) as f:
                        summaryLine = f.readline().strip()
                        #logopts["pdb"]=logopts.get("pdb", "") + "|" + summaryLine
                        queryString.append(summaryLine)
                    
                outputfilelist = glob.glob('%s%s%s/*.propka' % (INSTALLDIR, TMPDIR, jobid))
                for i in range(0,len(outputfilelist)):
                    outputfilelist[i] = os.path.basename(outputfilelist[i])
                for extension in ["-typemap.html", ".pqr", ".in"]:
                    if extension != ".in" or apbs_input != False:
                        if extension == "-typemap.html" and typemap == False: 
                            continue
                        outputfilelist.append('%s%s' % (jobid, extension))
                for outputfile in outputfilelist:
                    print "<li><a href=%s%s%s/%s>%s</a></li>" % (WEBSITE, TMPDIR, jobid, outputfile, outputfile)
                
            logopts['queryPDB2PQR'] = '|'.join(queryString) 

                #for extension in ["-typemap.html", ".pqr", ".in"]:
                #    print "<li><a href=%s%s%s/%s%s>%s%s</a></li>" % (WEBSITE, TMPDIR, jobid, jobid, extension, jobid, extension)
        elif calctype=="apbs":
            if have_opal:
                for i in range(0,len(filelist)):
                    if filelist[i]._name[-3:]==".dx":
                        # compressing APBS OpenDX output files
                        currentpath = os.getcwd()
                        zipjobid = filelist[i]._name.split("-")[0]
                        urllib.urlretrieve(filelist[i]._url, '%s%s%s/%s' % (INSTALLDIR, TMPDIR, zipjobid, filelist[i]._name))
                        os.chdir('%s%s%s' % (INSTALLDIR, TMPDIR, zipjobid))
                        # making both the dx file and the compressed file (.gz) available in the directory  
                        syscommand = 'cp %s dxbkupfile' % (filelist[i]._name)
                        os.system(syscommand)
                        syscommand = 'gzip -9 ' + filelist[i]._name
                        os.system(syscommand)
                        syscommand = 'mv dxbkupfile %s' % (filelist[i]._name)
                        os.system(syscommand)
                        os.chdir(currentpath)
                        outputfilezip = filelist[i]._name + '.gz'
                        print "<li><a href=%s%s%s/%s>%s</a></li>" % (WEBSITE, TMPDIR, zipjobid, outputfilezip, outputfilezip)
            else:
                outputfilelist = glob.glob('%s%s%s/%s-*.dx' % (INSTALLDIR, TMPDIR, jobid, jobid))
                for outputfile in outputfilelist:
                    # compressing APBS OpenDX output files
                    currentpath = os.getcwd()
                    workingpath = os.path.dirname(outputfile)
                    os.chdir(workingpath)
                    # making both the dx file and the compressed file (.gz) available in the directory  
                    syscommand = 'cp %s dxbkupfile' % (os.path.basename(outputfile))
                    os.system(syscommand)
                    syscommand = 'gzip -9 ' + os.path.basename(outputfile)
                    os.system(syscommand)
                    syscommand = 'mv dxbkupfile %s' % (os.path.basename(outputfile))
                    os.system(syscommand)
                    os.chdir(currentpath) 
                    outputfilezip = outputfile+".gz"
                    print "<li><a href=%s%s%s/%s>%s</a></li>" % (WEBSITE, TMPDIR, jobid, os.path.basename(outputfilezip), os.path.basename(outputfilezip))
                    
            logopts['queryAPBS'] = '|'.join(queryString) 
        
        if calctype=="pdb2pqr":                            
            if have_opal:    
                pass
            else:
                outputfilelist = glob.glob('%s%s%s/pdb2pka_output/*.DAT' % (INSTALLDIR, TMPDIR, jobid))
                outputfilelist.extend(glob.glob('%s%s%s/pdb2pka_output/*.txt' % (INSTALLDIR, TMPDIR, jobid)))
                outputfilelist = [os.path.basename(outputfile) for outputfile in outputfilelist]
                if outputfilelist:
                    print "</ul></li>"
                    print "<li>PDB2PKA files<ul>"
                    for outputfile in outputfilelist:
                        print "<li><a href=%s%s%s/pdb2pka_output/%s>%s</a></li>" % (WEBSITE, TMPDIR, jobid, outputfile, outputfile)
       
        print "</ul></li>"
        print "<li>Runtime and debugging information<ul>"

        if have_opal:
            stdouturl = resp._stdOut
            stderrurl = resp._stdErr
        else:
            stdouturl = "%s%s%s/%s_stdout.txt" % (WEBSITE, TMPDIR, jobid, calctype)
            stderrurl = "%s%s%s/%s_stderr.txt" % (WEBSITE, TMPDIR, jobid, calctype)

        print "<li><a href=%s>Program output (stdout)</a></li>" % stdouturl
        print "<li><a href=%s>Program errors and warnings (stderr)</a></li>" % stderrurl

        print "</ul></li></ul>"


        #if have_opal:
        #    resp = appServicePort.getOutputs(getOutputsRequest(jobid))
        #    for opalfile in resp._outputFile:
        #        if opalfile._name[-8:]!="-input.p":
        #            print "<li><a href=%s>%s</a></li>" % (opalfile._url, opalfile._name)
        #    print "<li><a href=%s>Standard output</a></li>" % (resp._stdOut)
        #    print "<li><a href=%s>Standard error</a></li>" % (resp._stdErr)
        #else:
        #    for line in cp[1:]:
        #        line = os.path.basename(line)
        #        if line[-8:]!="-input.p":
        #            if line[-11:]=="_stdout.txt":
        #                printname = "Standard output"
        #            elif line[-11:]=="_stderr.txt":
        #                printname = "Standard error"
        #            else:
        #                printname = line
        #            print "<li><a href=%s>%s</a></li>" % (WEBSITE+TMPDIR+jobid+"/"+line,printname)

        if calctype=="pdb2pqr" and apbs_input and HAVE_APBS:
            print "</ul></p><hr><p><b><a href=%s>Click here</a> to run APBS with your results.</b></p>" % nexturl
        elif calctype=="apbs":
            print "</ul></p><hr><p><b><a href=%s>Click here</a> to visualize your results.</b></p>" % nexturl

    elif progress == "error":
        print "There was an error with your query request. This page will not refresh."
        
        print "</ul></li>"
        print "<li>Runtime and debugging information<ul>"
        
        if have_opal:    
            resp = appServicePort.getOutputs(getOutputsRequest(jobid))
            stdouturl = resp._stdOut
            stderrurl = resp._stdErr
        else:
            stdouturl = "%s%s%s/%s_stdout.txt" % (WEBSITE, TMPDIR, jobid, calctype)
            stderrurl = "%s%s%s/%s_stderr.txt" % (WEBSITE, TMPDIR, jobid, calctype)

        print "<li><a href=%s>Program output (stdout)</a></li>" % stdouturl
        print "<li><a href=%s>Program errors and warnings (stderr)</a></li>" % stderrurl

        print "</ul></li></ul>"

        
    elif progress == "running":
        print "Page will refresh in %d seconds<br />" % refresh
        print "<HR>"
        print "</ul></li>"
        print "<li>Runtime and debugging information<ul>"
        
        if have_opal:    
            resp = appServicePort.getOutputs(getOutputsRequest(jobid))
            stdouturl = resp._stdOut
            stderrurl = resp._stdErr
        else:
            stdouturl = "%s%s%s/%s_stdout.txt" % (WEBSITE, TMPDIR, jobid, calctype)
            stderrurl = "%s%s%s/%s_stderr.txt" % (WEBSITE, TMPDIR, jobid, calctype)

        print "<li><a href=%s>Program output (stdout)</a></li>" % stdouturl
        print "<li><a href=%s>Program errors and warnings (stderr)</a></li>" % stderrurl

        print "</ul></li></ul>"
        print "<small>Your results will appear at <a href=%s>this page</a>. If you want, you can bookmark it and come back later (note: results are only stored for approximately 12-24 hours).</small>" % resultsurl
    elif progress == "version_mismatch":
        print "The versions of APBS on the local server and on the Opal server do not match, so the calculation could not be completed"
        
    print "</P>"
    print "<script type=\"text/javascript\">"    
    for key in logopts:
        print getEventTrackingString('queryData', key, logopts[key]),
        #print "_gaq.push(['_trackPageview', '/main_cgi/has_%s_%s.html']);" % (key, logopts[key])
    print "</script>"
    print "</div> <!--end content div-->"
    print "</BODY>"
    print "</HTML>"

if __name__ == "__main__" and os.environ.has_key("REQUEST_METHOD"):
    """ Determine if called from command line or CGI """
    refresh=30

    if not form.has_key("jobid") and form["calctype"].value=="pdb2pqr":
        print "Content-type: text/html\n\n"
        print printheader("PDB2PQR Job Status - Error")
        text="<BODY>\n"
        text+="\t<H2>Missing jobid field</H2>\n"
        text+="\t<P>Your request url is missing the jobid field</P>\n"
        text += "<script type=\"text/javascript\">"
        text += "var gaJsHost = ((\"https:\" == document.location.protocol) ? \"https://ssl.\" : \"http://www.\");"
        text += "document.write(unescape(\"%3Cscript src=\'\" + gaJsHost + \"google-analytics.com/ga.js\' type=\'text/javascript\'%3E%3C/script%3E\"));"
        text += "</script>"
        text += "<script type=\"text/javascript\">"
        text += "try {"
        text += "var pageTracker = _gat._getTracker(\"UA-11026338-3\");"
        text += "pageTracker._trackPageview();"
        text += "} catch(err) {}</script>"
        text+="</BODY>\n</HTML>"
        print text
        sys.exit(2)


    if (form["calctype"].value=="pdb2pqr" and HAVE_PDB2PQR_OPAL=="1") or (form["calctype"].value=="apbs" and APBS_OPAL_URL!=""):
        have_opal = True
        from AppService_client import AppServiceLocator, getAppMetadataRequest, launchJobRequest, launchJobBlockingRequest, getOutputAsBase64ByNameRequest, queryStatusRequest, getOutputsRequest
        from AppService_types import ns0
        from ZSI.TC import String
    else:
        have_opal = False

    mainCGI()
