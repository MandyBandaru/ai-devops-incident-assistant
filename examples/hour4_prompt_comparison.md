
# Hour 4: Jenkins Prompt Comparison

## Incident
- Stage: Build
- Environment: Linux Jenkins agent
- Recent change: Build moved to a new agent
- Error: `mvn: command not found`

## Test 1: Weak prompt
Prompt: My Jenkins pipeline failed. Fix it.

- Did it explain the error? YES
- Did it separate facts from possible causes? No
- Did it provide useful diagnostic steps? no
- Did it make assumptions? yes

My observations:
It has provided some steps and solutions which i need to understand those and resolve the error looks like i need to put some time in to that to  resolve

## Test 2: Structured prompt
Prompt: See prompts/jenkins_structured.md

- Did it explain the error? yes
- Did it separate facts from possible causes? yes
- Did it provide useful diagnostic steps? yes
- Did it make assumptions? no

My observations:
Clear Explaination of error 
it seprated facts from possible cause
also provided diagnostic steps ans
no Assumptions only recommendeations


## Conclusion
Which prompt was more useful and why?

i see prompt 2 is more use ful it make the things simplified saving time to resolve the error with out putting much time on researching from the output provided by ai
