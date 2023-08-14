import hudson.model.*
import hudson.maven.*
import hudson.tasks.*
import jenkins.model.Jenkins
import hudson.maven.reporters.*
import hudson.plugins.emailext.*

// name = "test_master_builder_project"
// //If we want to add more then one job
def items = new LinkedHashSet();
// def job = Hudson.instance.getJob(name)
Jenkins.instance.getAllItems(Job.class).each {
    items.add(it);
};
def jobsList = []

def findCause(upStreamBuild) {
    //Check if the build was triggered by SCM change
    scmCause = upStreamBuild.getCause(hudson.triggers.SCMTrigger.SCMTriggerCause)
    if (scmCause != null) {
        return scmCause.getShortDescription()
    }
    
    //Check if the build was triggered by timer
    timerCause = upStreamBuild.getCause(hudson.triggers.TimerTrigger.TimerTriggerCause)
    if (timerCause != null) {
        return timerCause.getShortDescription()
    }
    
    //Check if the build was triggered by some jenkins user
    usercause = upStreamBuild.getCause(hudson.model.Cause.UserIdCause.class)
    if (usercause != null) {
        return usercause.getUserId()
    }
    
    //Check if the build was triggered by some jenkins project(job)
    upstreamcause = upStreamBuild.getCause(hudson.model.Cause.UpstreamCause.class)
    if (upstreamcause != null) {
        job = Jenkins.getInstance().getItemByFullName(upstreamcause.getUpstreamProject(), hudson.model.Job.class)
        if (job != null) {
            upstream = job.getBuildByNumber(upstreamcause.getUpstreamBuild())
            if (upstream != null) {
                return upstream
            }
        }
    }
    return;
}

// Iterate through each item.
items.each { item ->
    try {
        def jobsMap = [:]
        def job_data = Jenkins.instance.getItemByFullName(item.fullName)
        jobsMap["job"] = item.fullName
        
        //Check if job had atleast one build done
        if (job_data.getFirstBuild()) {
            first_job_num = job_data.getFirstBuild().getNumber()
            def upStreamBuild = Jenkins.getInstance().getItemByFullName(item.fullName).getBuildByNumber(first_job_num)
            
            jobsMap["firstJobNum"] = first_job_num
            jobsMap["firstBuildTime"] = upStreamBuild.getTime()
            jobsMap["firstBuildCause"] = "${findCause(upStreamBuild)}"
        } else {
            jobsMap["firstJobNum"] = "Null"
        }

        if (job_data.getLastBuild()) {
            last_job_num = job_data.getLastBuild().getNumber()
            def upStreamBuild = Jenkins.getInstance().getItemByFullName(item.fullName).getBuildByNumber(last_job_num)
            
            jobsMap["lastJobNum"] = last_job_num
            jobsMap["lastBuildTime"] = upStreamBuild.getTime()
            jobsMap["lastJobCause"] = "${findCause(upStreamBuild)}"
            
            //Check if job had atleast one successful build
            if (job_data.getLastSuccessfulBuild()) {
                jobsMap["lastSuccessNum"] = job_data.getLastSuccessfulBuild().getNumber()
                jobsMap["lastSuccessResult"] = true
            } else {
                jobsMap["lastSuccessNum"] = "Null"
                jobsMap["lastSuccessResult"] = false
            }
        } else {
            jobsMap["lastBuildNum"] = "Null"
        }
        jobsList << jobsMap
    } catch (Exception e) {
        println ' Ignoring exception ' + e
    }
}

println new groovy.json.JsonBuilder(jobsList)

return;