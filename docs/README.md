## Problem Statement 

 Troubleshooting Cisco Contact Center solutions is becoming difficult due to complex integration. With constant increase in demand for cloud managed and cloud hosted solutions, existing serviceability solutions and practices (on Cisco Contact Center Products) are proving to be inefficient.

> This project intent towards exploring alternate serviceability solutions and practices for managing/    servicing Cisco CC Products and Solutions.


## Project overview

> Identify contact center call behaviors based on signaling attributes, create unique call signatures based on signaling attributes and logically group them based on call signatures.

Solution with have hybrid approach,
- Product agnostic approach of identifying call behaviors based on call signaling attributes and logically grouping them based on unique behavior patterns.
- Product specific approach where call behavior patterns are identified based on product architecture

Logically combine 2 patterns to derive call context and unique call signatures

## Audience

> Cisco Contact Center product/solution teams (TAC) and Cisco managed contact center solution support group

## Technologies Used

![Technologies](_media\technologies.png  ':size=650x350')

We used HTML, CSS, JS for the frontend part and Flask application to connect the front end to the server side. We used this application to provide the following features :
- Take input logs from the user and store processed results in the database.
- Show the per call visualization in the form of a ladder diagram.
- Intelligent filtering feature.
- Giving the users option to add more signatures.
- Display the matched signatures per call.

## Call flow Visualization

A call flow is a flow diagram which is an ideal way to show how a media session carried over two endpoints.

![LadderDiagram](_media\LadderDiagram.png ) 


![LadderDiagram1](_media\LadderDiagram1.png) 

Select the calls you want to check, then we should be able to see the ladder diagram visualizing the call flow sequence between different user agents for each call as shown in the above examples. It simplifies the identification of different transactions and dialogs involved in a call, and will be useful for troubleshooting as well.


SIP is a call signalling mechanism and one of the fundamental building blocks of today modern VoIP communication. And SDP is always a focal point to check media related issues in VoIP. An SDP message consists of three sections, detailing the session, timing, and media descriptions. Each message may contain multiple timing and media descriptions.

<div style="margin-left: 125px;">

![MsgDescription](_media\MsgDescription.png ':size=500x250')

![MsgDescription1](_media\MsgDescription1.png ':size=500x250')

</div>

Clicking on each message shows the description as shown in the above images, highlighting some important haeaders such as call id, media line, codecs for SIP and SDP messages; and call guid, dialog id for cvp messages.

## Functionalities

> <h4><bold>Displays calls list</bold></h4>

![Call Summary Table](_media\CallSummaryTable.png)

For each call log selected, We can see the information below for each call:
- Call guid which uniquely identifies each call.
- Caller ID and Callee ID in the ANI and DNIS columns.
- Details link which displays the ladder diagram.
- A link to get the matched signatures.

> <h4><bold>Intelligent Call Filtering</bold></h4>

    'Parameter'=='Value'

The above format is used as a filter. Below is an example for filtering.

![Filter](_media\Filter.png)

Below image shows the filtering output.

![Filteroutput](_media\Filteroutput.png)


> <h4><bold>Signatures</bold></h4>

Below image shows a portal for adding new signatures. Added signatures are shown in a tabular format with a description for each.

![Signature](_media\Signature.png)

## APIs used

- Gets the analyzed results of the selected log file which are displayed in the form of the call summary table.
```
    route("/Files-History/analyze")
```
- It returns the svg format of ladder diagram for the respective call.
```
    route("/Call-Summary/details")
```
- It fetches the description for the message selected.
```
    route("/Call-Summary/message")
```
- Below API is used for uploading the files in the web application. It also focuses on handling the zipped log files. 
```
    route("/Files-History/upload", methods=["POST"])
```
- It renders the call flow sequence in the form of a ladder diagram for the respective call.
```
    route('/diagram-page',methods=["GET"])
```
- It returns the filtered result for the given query. Filtering is done per log file.
```
    route("/Call-Summary/filter", methods=["POST"])
```
- Gets all the signatures with their description from the database.
```
    route("/get-signatures")
```
- Returns the matched signatures for the respective call.
```
    route("/Call-Summary/signature")
```

## Team

![Team](_media\Team.png ':size=600x300') 



