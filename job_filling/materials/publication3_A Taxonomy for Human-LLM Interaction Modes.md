# publication3_A Taxonomy for Human-LLM Interaction Modes

A Taxonomy for Human-LLM Interaction Modes: An Initial
Exploration
Jie Gao, Simret Araya Gebreegziabher,
Kenny Tsu Wei Choo, Toby Jia-Jun Li, Simon Tangi Perrault, and Thomas W. Malone
December 1, 2025
Contribution:
As large language models rapidly transformed how people interact with AI systems, the HCI
community lacked a unified conceptual framework to describe the diverse and rapidly emerging human-
LLM interaction designs. This paper provides one of the earliest systematic efforts to build such a
taxonomy by conducting a structured literature review across major HCI venues (CHI, CSCW, UIST,
IUI; see page 2, Table 1), followed by iterative coding and refinement of interaction characteristics (page
2). Through this analysis, the paper identifies four temporal phases in a human-LLM interaction flow,
planning, facilitating, iterating, and testing, and introduces an initial exploration of taxonomy of four
primary interaction modes:
• Standard Prompting,
• User Interface–based Interaction,
• Context-based Interaction
• Agent Facilitator
Each mode is further articulated using the “Who, What, When, How” framework, offering a struc-
tured lens for understanding both current and future interaction designs. By synthesizing patterns
across dozens of HCI systems, the paper provides the first cohesive theoretical scaffolding for classifying
and reasoning about human-LLM interactions.
This taxonomy serves two major contributions.
Methodologically, it offers a systematic vo-
cabulary and design space that helps researchers and practitioners analyze, compare, and generate
new interaction paradigms. Practically, it highlights previously underexplored combinations of rea-
soning, UI design, context control, and agent-facilitated collaboration, opening new possibilities for
next-generation LLM-powered systems (see discussion on pages 6–7).
Significance:
As one of the earliest papers to frame human-LLM interaction holistically, this work has supported
subsequent innovations in prompt engineering tools, visual programming for LLMs, agent-based col-
laboration, and multimodal AI interfaces. As of Dec 1, 2025, this paper has received 76 citations,
making it an initial but influential foundation for the growing research area of human-LLM interaction
design.
1

A Taxonomy for Human-LLM Interaction Modes: An Initial 
Exploration 
Jie Gao∗ 
jie.gao@smart.mit.edu 
Singapore-MIT Alliance for Research 
and Technology 
Singapore 
Toby Jia-Jun Li 
toby.j.li@nd.edu 
University of Notre Dame 
Notre Dame, Indiana, USA 
Simret Araya Gebreegziabher∗ 
sgebreeg@nd.edu 
University of Notre Dame 
Notre Dame, Indiana, USA 
Simon Tangi Perrault 
perrault.simon@gmail.com 
Singapore University of Technology 
and Design 
Singapore 
Kenny Tsu Wei Choo 
kenny@kennychoo.net 
Singapore University of Technology 
and Design 
Singapore 
Thomas W. Malone 
malone@mit.edu 
Massachusetts Institute of Technology 
Cambridge, Massachusetts, USA 
ABSTRACT 
With ChatGPT’s release, conversational prompting has become 
the most popular form of human-LLM interaction. However, its 
efectiveness is limited for more complex tasks involving reason­
ing, creativity, and iteration. Through a systematic analysis of HCI 
papers published since 2021, we identifed four key phases in the 
human-LLM interaction fow—planning, facilitating, iterating, and 
testing—to precisely understand the dynamics of this process. Addi­
tionally, we have developed a taxonomy of four primary interaction 
modes: Mode 1: Standard Prompting, Mode 2: User Interface, Mode 
3: Context-based, and Mode 4: Agent Facilitator. This taxonomy 
was further enriched using the “5W1H” guideline method, which 
involved a detailed examination of defnitions, participant roles 
(Who), the phases that happened (When), human objectives and 
LLM abilities (What), and the mechanics of each interaction mode 
(How). We anticipate this taxonomy will contribute to the future 
design and evaluation of human-LLM interaction. 
CCS CONCEPTS 
• Human-centered computing → Natural language interfaces. 
KEYWORDS 
Taxonomy, Human-LLM Interaction, Large Language Models 
ACM Reference Format: 
Jie Gao, Simret Araya Gebreegziabher, Kenny Tsu Wei Choo, Toby Jia-
Jun Li, Simon Tangi Perrault, and Thomas W. Malone. 2024. A Taxonomy 
for Human-LLM Interaction Modes: An Initial Exploration. In Extended 
Abstracts of the CHI Conference on Human Factors in Computing Systems 
(CHI EA ’24), May 11–16, 2024, Honolulu, HI, USA. ACM, New York, NY, USA, 
11 pages. https://doi.org/10.1145/3613905.3650786 
∗Both authors contributed equally to this paper. 
Permission to make digital or hard copies of part or all of this work for personal or 
classroom use is granted without fee provided that copies are not made or distributed 
for proft or commercial advantage and that copies bear this notice and the full citation 
on the frst page. Copyrights for third-party components of this work must be honored. 
For all other uses, contact the owner/author(s). 
CHI EA ’24, May 11–16, 2024, Honolulu, HI, USA 
© 2024 Copyright held by the owner/author(s). 
ACM ISBN 979-8-4007-0331-7/24/05 
https://doi.org/10.1145/3613905.3650786 
1 INTRODUCTION AND BACKGROUND 
Every use of computers involves an interaction mode—a pattern 
of interaction between the user and the computer. This concept 
has evolved signifcantly, starting from command-line interfaces on 
early teletypes, advancing to the direct manipulation of on-screen 
images, and progressing to engaging conversations with chatbots, 
among others [60]. 
Since the introduction of Large Language Models (LLMs), es­
pecially ChatGPT, conversational interactions have become the 
"default" interaction mode for the interaction between human users 
and LLMs. This extends to other notable platforms like Claude1, 
Gemini2, and Llama 23, among others. This interaction is based on 
prompts—specifc instructions given to an LLM that allow it to grasp 
the user’s intent and then generate meaningful outcomes through di­
alogue. Thus, the creation of high-quality, well-considered prompts 
for the dialogue is critical for enhancing outcomes. 
Moreover, intricately designed prompts enable the execution of 
complex tasks, such as solving mathematical problems, writing, and 
coding. The design strategies include zero-shot [36], few-shot [45], 
chain-of-thought techniques [68], etc. Furthermore, White et al. [69] 
have identifed a series of prompt patterns—similar to software 
design patterns [19, 57]—that can be employed to construct com­
plex prompts. For example, the "fipped interaction" pattern, where 
LLMs initiate questions instead of merely producing outputs; the 
"gameplay pattern", generating output in game format; and the "in­
fnite generation pattern", enabling continuous output generation 
without repeated user prompts. 
Recently, HCI researchers have pushed the boundaries of con­
versational interaction capabilities through diverse human-LLM 
interaction designs. The key strategy is to leverage various HCI 
techniques like visual programming and direct manipulation, to 
develop complex prompts. These prompts signifcantly enhance 
LLMs, equipping them with sophisticated capabilities for complex 
tasks, including argumentative writing [80], brainstorming [27, 63], 
and more. However, they primarily focus on developing specifc 
interaction modes, often overlooking a more comprehensive frame­
work that encompasses various interaction perspectives. Exploring 
1https://claude.ai/chats
2https://gemini.google.com/app 
3https://www.llama2.ai/

CHI EA ’24, May 11–16, 2024, Honolulu, HI, USA 
Jie Gao, Simret Araya Gebreegziabher et al. 
Table 1: Data Collection. The table shows the initial count of papers at Stage 1 and the number of papers remaining at Stage 2 
after the fltering process. 
CHI’23 
CHI’22 
CHI’21 
UIST’23 
UIST’22 
UIST’21 
CSCW’23 
CSCW’22 
CSCW’21 
IU
9
I’23 
IUI’22 
IUI’21 
Total 
Stage 1: Initial Searching 
23 
19 
8
7 
5 
10 
5 
12 
Stage 2: (Post) Paper Filtering 
43
19 
10 
5 
12
11
4 
3 
11
4 
2 
4 
6 
3 
2 
73 
164 
the various types of interaction modes within such a framework is 
promising, yet remains largely underexplored. 
In this work, we investigate the following research questions 
about the human-LLM interaction: 
• RQ1: What are the diferent phases in a human-LLM interac­
tion fow? Although much research has started to reference 
"human-LLM interaction" 4, a precise defnition of this term 
remains vague. What exactly does it encompass? Therefore, 
gaining a more accurate understanding of its nature, includ­
ing the phases within a “Human-LLM Interaction" fow, is 
crucial. 
• RQ2: How can the various interaction modes between humans 
and LLMs be categorized? Is it possible to structure these into 
a taxonomy? 
To answer our research questions, we performed a systematic 
review of existing literature in HCI venues published since 2021, 
including CHI, CSCW, UIST, and IUI. Our analysis of current lit­
erature on LLM-powered tools and systems has led to the identif­
cation of four crucial temporal phases in these interaction fows, 
namely planning, facilitating, iterating, and testing. Additionally, 
our research introduces a detailed, structured taxonomy that en­
capsulates four modes of interaction between humans and LLMs, 
including Mode 1: Standard Prompting, Mode 2: User Interface, Mode 
3: Context-based, and Mode 4: Agent Facilitator. We anticipate that 
these interaction modes, initially foundational in writing and cod­
ing, will become crucial across various tasks where prompts act 
as the primary mechanism driving system functionality, e.g., in 
image and video generation. As this paper begins an exploration, 
we anticipate its scope will broaden with the evolving applications 
of LLMs, thereby infuencing the future of human-LLM interaction. 
2 METHOD 
2.1 Data Collection 
Our data collection methodology is informed by a systematic lit­
erature review protocol [32], which focuses on manual searches 
across main HCI venues, including conference proceedings like 
CHI, CSCW, UIST, and IUI. The collection is conducted through 
two stages. 
2.1.1 Stage 1: Initial Searching. Two authors focused on papers that 
mentioned key terms including “Large Language Models”, “LLMs”, 
“Natural Language”, “prompt/prompting”, “generative AI”, “GPT” and 
“human-AI”. The inclusion criteria primarily targeted papers that 
4See From Thought to Prompt: Cognitive Design Challenges in Human-LLM 
Interactions: https://www.aalto.f/en/events/from-thought-to-prompt-cognitive­
design-challenges-in-human-llm-interactions, Call for papers for human-LLM 
interaction: https://human-llm-interaction.github.io/workshop/hri24/call-for-papers, 
Low-code LLM [9], and many others. 
1) proposed new platforms or software integrating LLMs, 2) intro­
duced novel interaction techniques with LLMs; and 3) included a 
few studies on AI agents, which, although not using LLMs, are still 
relevant to the topic. Moreover, our focus was on research published 
after 2021, aligning with the period when LLMs gained widespread 
popularity. In total, there were 164 papers were identifed. Table 1 
presents the number of papers under each venue. 
2.1.2 Stage 2: Paper Filtering. After collecting the papers, we have 
performed a deep fltering process, aiming to focus on the most 
relevant contributions. The two authors independently summarized 
and evaluated the collected papers, noting their relevance and con­
tributions, and documented the rationale behind their pertinence. 
Following this, the authors convened to discuss their fndings and 
collectively decide on the inclusion or exclusion of each paper. In 
total, 73 papers were left. 
2.2 Constructing the Taxonomy 
2.2.1 Stage 1: Development of A Primary Taxonomy. Initially, we 
focused on the types of interactions each paper described. After 
reviewing and discussing the literature, primary categories were 
identifed (see Appendix Table 3). For each category, we adapted 
the “5W1H” guideline 5, and ultimately, we found that only four 
out of the fve dimensions are necessary: 
• Who: the participated roles in the human-LLM interaction, 
aiming to understand who is involved and the tasks they 
perform within the interaction fow. 
• What: the objectives of human engagement and the ad­
vanced capabilities LLMs gain through augmentation. 
• When: the phases at which LLM capabilities manifest during 
the interaction fow. 
• How: the underlying mechanisms and methods of these 
interactions. 
2.2.2 Stage 2: Systematic Annotation of Each Paper and Refinement 
of the Primary Taxonomy. After initially developing the basic tax­
onomy, the two authors independently annotated more papers, 
incorporating more categories and detailed dimensions into the tax­
onomy. Next, they had iterative discussions to address ambiguities 
and discrepancies, gradually refning the classifcation criteria for 
greater clarity. Lastly, with the refned and more structured taxon­
omy in hand, the authors proceeded to code the remaining papers 
for the complete classifcation (see Appendix Table 2). Through 
this iterative process, we have developed a taxonomy that cap­
tures the intricate details and various types of current human-LLM 
interactions. 
5https://ipma.world/5ws-1h-a-technique-to-improve-project-management­
efciencies/

A Taxonomy for Human-LLM Interaction Modes: An Initial Exploration 
CHI EA ’24, May 11–16, 2024, Honolulu, HI, USA 
➕
Human
LLM
Users interact with LLMs through 
text-based conversational prompting
Who:
When:
What:
How:
Question Answering, Flipped Interaction, 
Decomposed Prompting, etc.
Example:
Prompt Pattern Catalog (White et al. 2023)
Definition: 
➕
➕
Reasoning
Human
LLM
Users interact with LLMs through text-based 
conversational prompting, facilitating a dialogue 
involving reasoning 
Who:
Definition: 
When:
What:
How:
Example:
Facilitating
Iterating
Facilitating
Break the task into manageable steps for 
sequential execution with user intervention 
at each stage.
Standard Prompting
1.
1.2 Text-based Converastional Prompting  with Reasoning
1.1. Text-based Conversational Prompting
AI Chains (Wu et al. 2022)
Human
Gives effective instuctions to LLM 
and judges results
LLM
Understanding, generating text, in 
order to perform users’ given tasks.
Programmer’s Assistant (Ross et al. 2023)
ChatGPT, Claude, LLama 2, Gemini, etc. 
Human
LLM
Use LLMs to complete complex tasks with 
high-level reasoning
Complete complex tasks like reasoning
Figure 1: Mode 1: Standard Prompting. 
3 RESULTS 
3.1 RQ1: Four phases of a human-LLM 
interaction fow 
During the development of the taxonomy, we gained a clearer 
understanding of the four phases in which LLM assistance typically 
occurs, including planning, facilitating, iterating, and testing. 
(1) Planning (before an interaction): This phase includes strate­
gizing the entire interaction beyond basic conversational 
exchanges. In this stage there is a focus to determine the 
goals of the interaction, and the steps needed to achieve 
these goals (e.g., determining specifc inputs and outputs for 
each step). 
(2) Facilitating (during an interaction): This phase, perhaps the 
most prevalent, involves assisting users in formulating or 
completing their interaction proposals, such as text com­
pletion. An additional example includes users refning their 
prompts by asking more in-depth questions or incorporating 
extra details during conversations with LLMs to achieve their 
objectives. Furthermore, users evaluate the LLM’s varied sug­
gestions, ultimately accepting or rejecting these proposals 
to fulfll their goals. 
(3) Iterating (refning an established interaction): After establish­
ing and completing an initial interaction fow, users refne 
and enhance this process through successive adjustments, 
eliminating the need for further conversation. This can in­
volve iterating over the existing prompts and instructions or 
the outputs through diferent afordances. 
(4) Testing (testing a defned interaction): This phase generates 
and evaluates diverse responses to variations of user-designed 
prompts. Such testing is crucial for understanding the breadth 
and depth of the interactions. 
3.2 RQ2: Taxonomy 
3.2.1 Mode 1: Standard Prompting. Standard Prompting (Fig­
ure 1) represents the foundational and widely adopted interaction 
mode between humans and LLMs. 
Mode 1.1. Text-based Conversational Prompting. This mode 
employs a standard, conversational approach where users design 
and input prompts, to which the LLM responds with textual out­
puts [85]. This include single-turn conversation [61] and multiple-
turn conversations [7]. Through each interaction users dynami­
cally elicit responses from the LLM to steer the conversation to­
wards achieving their desired outcomes. Therefore, both the user’s 
prompts and the LLM’s responses evolve to more precisely address 
the task at hand (such as seeking answers or ideation). 
In fact, many platforms, including ChatGPT, Claude, LLama 2, 
and Gemini, employ this conversational prompting method. From 
the literature, Programmer’s Assistant [56] provides an interface 
that allows users to interact with the model conversationally. This 
facilitates understanding code and generating alternative responses 
through conversational interactions during coding. Another method 
employs conversational prompting, which can be executed in a 
"single-turn conversation", involving inputting text into an LLM, 
which then returns suggestions or completes the text. One example 
is the OpenAI Playground; similarly, literature such as CoAuthor 
leverages LLMs to ofer writing suggestions based on the user’s 
input text [40]. 
However, this mode often has limitations, as it allows users 
to input only a limited amount of information through single or 
multiple-turn prompts. Executing higher-level tasks, such as plan­
ning and testing multiple variations, can be challenging. Further­
more, it may also be susceptible to ambiguity and misalignment 
in interpreting intent [1]. Therefore, in the original conversational 
prompting, prompts must be strategically designed in various ways 
to further discern user intent. This includes fipped interactions [1] 
or gameplay interaction, etc. [69].

CHI EA ’24, May 11–16, 2024, Honolulu, HI, USA 
Jie Gao, Simret Araya Gebreegziabher et al. 
➕
➕
Human
LLM
UI for input
Who:
When:
What:
How:
Example:
Definition: 
Facilitating
Users interact with LLM by inputting 
structured prompts through a interface
Using interface design to structure the 
input of zero-shot, few-shot examples, etc. 
Chocie Over Control (Dang et al.2023)
PromptMaker (Jiang et al.2022)
Who:
When:
What:
How:
Example:
Definition: Users interact with LLM following the 
establishment of an interaction process 
to enhance it.
➕
➕
Human
LLM UI for input/output
Iterating
Debugging a predefined baseline interaction;
Error labelling and regenerating
Why Johnny Can’t Prompt 
(Zamfrescu-Pereira et al. 2023)
Who:
When:
What:
How:
Example:
Definition: Users interact with LLM to experiment with 
different prompts in interaction process
➕
➕
Human
LLM
UI for input/output
Testing
Leveraging an interface to generate a series of 
prompt variations through simple clicks.
VISAR (Zhang et al. 2023)
GANzilla (Evirgen et al. 2022)
Who:
When:
What:
How:
Example:
Definition: Users interact with LLM through text prompts, 
requesting LLM to return outcomes via an interface
Designing an interface to show more affordances 
of controls through different forms UI designs
➕
➕
Human
LLM
UI for output
Iterating
GenLine (Jiang et al. 2022)
User Interface
2.
2.1 UI for Structured Input
2.3 UI for Iteration of Interaction
2.4 UI for Testing of Interaction
2.2 UI for Varing Output
➕
➕
Reasoning
Human
LLM
UI for output
➕
Users interact with LLM using interfaces that 
enable visual programming and mind mapping, 
streamlining prompt organization with reasoning 
techniques.
Who:
Definition: 
When:
What:
How:
Example:
Facilitating
Decompose prompts for LLM's step-by-step 
execution with user intervention, organized via 
visual tools like visual programming and mind maps.
PromptChainer (Wu et al. 2022)
Graphologue (Jiang et al.2023)
2.5 UI for Reasoning
Human
LLM
Create consistent and structured 
input prompts
Generate results for structured 
prompts
Human
LLM
Have more affordances of control 
to modify LLM generated results
Generate LLMs' results with more 
complexity, structures, layers
Human
LLM
Facilitating
Refine the current interaction to 
better align with their goals
Generate better results
Human
LLM
Testing the effectiveness of various 
prompts within a manageable timeframe.
Simultaneously producing various 
output versions.
Human
LLM
Utilizing reasoning techniques like visual 
programming to organize thoughts
Generating contents with higher level 
of abstraction, creativity 
Figure 2: Mode 2: User Interface. 
Mode 1.2. Text-based Conversational Prompting with Rea­
soning. While linear conversational interaction with LLMs lever­
ages the LLM’s capability to discern user intent and generate or 
modify outputs accordingly, researchers have proposed augmenting 
LLMs with enhanced reasoning abilities to expand their problem-
solving capacity beyond basic inquiries such as mathematical problem-
solving [42] and argumentative writing [48]. The foundational 
approach to reasoning in text involves employing the Chain-of-
Thought method [67]. This approach breaks down complex tasks 
into smaller, more manageable steps, using the output from previ­
ous steps to inform subsequent ones. While important and distinct 
from standard text-based conversational prompting, we found that 
this mode is primarily linked to UI design in HCI. We will provide 
more examples in Mode 2.5 in Section 3.2.2. 
3.2.2 Mode 2: User Interface (UI). Uer Interface (Figure 2) is 
a pivotal and practical means to enhance LLMs with advanced 
capabilities. 
Mode 2.1. UI for Structured Prompts Input. This approach 
enhances LLM inputs through a structured UI. For instance, distinct 
UI elements can be employed to input various components of a 
prompt, such as zero-shot, few-shot examples, and specifc con­
straints. This approach ensures that each prompt is created easily 
and consistently, allowing users to concentrate on the key contents 
rather than spending time crafting a comprehensible prompt. For 
instance, Jiang et al.[24] introduced PromptMaker, a tool that com­
bines Prefxes, Settings, and Examples to create structured prompt 
inputs. Similarly, Dang et al.[14] developed UI variants that inte­
grate user instructions with the standard prompting, enhancing 
more nuanced user-model interaction. 
Mode 2.2. UI for Varying Output. UI design can further en­
hance LLM outputs by providing users with options to specify 
output formats and controls. These include selecting the size, pick­
ing the color, or choosing button layouts via the output interface. 
The aim is to enable LLMs to produce results that are not only 
more functional but also more complex, structured, and layered, 
providing greater depth and utility in the generated content. A 
typical example is GenLine, developed by Jiang et al.[26], which 
enables users to generate CSS styles, such as button-style HTML 
code, and ofers an interface for users to choose whether to accept 
the generated style. A variation of this tool is GenForm[25], which 
facilitates the structured generation of mixed outputs, including

A Taxonomy for Human-LLM Interaction Modes: An Initial Exploration 
CHI EA ’24, May 11–16, 2024, Honolulu, HI, USA 
➕
➕
Human
LLM
Explicit Context
Who:
When:
What:
How:
Example:
Definition: 
➕
➕
Human
LLM
Implicit Context
Who:
When:
What:
How:
Example:
Definition: 
Users interact with LLM through explictly 
defined contextual information
Users command LLM implicitly, allowing it to 
self-determine task execution with minimal 
guidance
Planning
Facilitating
Asking LLMs to perform tasks with specific 
rules (e.g., coding with codebook in 
qualitative coding)
Codebook-based prompting 
(Xiao et al.2023)
Prompting LLM with specific examples;
Asking LLM to perform tasks as a role 
(role play)
Facilitating
Example-based prompting (Xiao et al.2023)
From Gap to Synergy (Chen et al. 2022)
Context-based
3.
3.1 Explicit Context
3.2 Implicit Context
Human
LLM
Creating precise rules or commands 
to define the context and steer 
responses in targeted directions.
Generating response that align 
with the specific context
AutoSurveyGPT (Xiao et al.2023)
Human
LLM
Directing interactions along specific paths 
by implicit contextual instructions.
Identifying specific tasks from general 
instructions and generating outcomes.
Figure 3: Mode 3: Context-based. 
HTML, JavaScript, and CSS code, through a form interface. Con­
trasting with PromptMaker’s focus on structuring prompt inputs 
through UI design, GenLine and GenForm prioritize transforming 
code generation into structured outputs for enhanced user con­
sumption. 
Mode 2.3. UI for Iteration of Interaction. UI design can signif­
icantly improve the iterative aspects of an interaction fow, incor­
porating features like debugging, error labeling, regenerating, and 
self-repairing. Such UI enhancements allow users to refne their 
original interaction fows, leading to improved fnal or intermediate 
outputs [6, 43]. For instance, BotDesigner [78] aids users in refning 
human-LLM interactions, such as recipe conversations. It allows 
users to identify and label errors within the conversation via its 
interface and ofers a "retry" button to regenerate the intermediate 
output, ensuring the integrity of the original interaction. 
Mode 2.4. UI for Testing of Interaction. UI design is employed 
to facilitate the testing of various prompt variations within an in­
teraction fow. This capability is particularly useful for quickly pro­
totyping complex artifacts, such as long writings, allowing users 
to experiment with and refne their creations with diferent in­
puts, prompts, and models. A typical example is VISAR [80], which 
employs visual programming to give users control over the frame­
work of argumentative writing and facilitates rapid prototyping 
of prompt ideas, enabling quick testing of writing organization. 
Similarly, Kim et al. [35] introduced a new interface that allows end 
users to experiment with model confgurations and inputs using 
object-oriented interaction. 
Mode 2.5. UI for Reasoning. Expanding upon the basic forms of 
reasoning augmentation in Mode 1.2 in Section 3.2.1, a signifcant 
advancement involves incorporating direct manipulation through 
UI design into the Chain-of-Thought process. This approach allows 
users to actively participate in the reasoning sequence, providing 
immediate control at intermediate steps to alter the direction or 
nature of the reasoning. Users might seek not only to create the rea­
soning process but also to reorganize reasoning blocks in a manner 
that aligns with their unique thought processes. The objective is to 
tackle complex tasks, yet with enhanced control, customization, and 
precision. This is facilitated by employing visual programming tech­
niques, such as chain designs [3, 71, 72] and mind maps [27, 63, 80], 
enabling a more interactive and user-defned reasoning framework. 
While there may be some overlap with other modes, such as Mode 
2.2 UI for Varying Output, we classify this as a distinct submode due 
to its unique blend of reasoning and UI design. 
3.2.3 Mode 3: Context-based. Context-based mode focuses on 
augmenting the system with specifc contextual understandings 
(Figure 3). Although this mode is less widespread and dominant 
compared to Mode 1: Standard Prompting and Mode 2: User Interface, 
it may serve as a key direction in design, potentially inspiring 
further work within two distinct approaches—explicitly defned 
rules/contexts or implicit contexts. 
Mode 3.1. Explicit Context. Augmenting LLMs with an explicit 
context involves prompting to process and respond to information 
based on predefned dimensions or contextual rules. For instance, 
codebook-centered prompting [76] enables researchers to provide 
LLMs with a codebook for qualitative analysis, outlining specifc 
design patterns in data. Similarly, AutoSurveyGPT [74] enables 
LLMs to automatically scan abstracts and extract keywords based 
on pre-defned commands and rules. 
Mode 3.2. Implicit Context. In contrast, augmenting LLMs with 
implicit context involves providing them with limited or general 
queries and commands, and then expecting them to infer how to per­
form tasks based on a few examples or by detecting the underlying 
context [62]. This approach demands the LLM’s interpretation of 
user intent and subtle signals, fostering a nuanced grasp of context 
for tasks needing profound contextual insight. Typical examples 
include role play and example-based prompting. In role play, 
users enhance LLMs’ output quality by assigning them specifc 
roles, such as a chatbot capable of refective thinking [37]. This 
method involves inputting detailed information profles, such as 
characteristics and areas of expertise, to closely simulate real expert

CHI EA ’24, May 11–16, 2024, Honolulu, HI, USA 
Jie Gao, Simret Araya Gebreegziabher et al. 
➕
➕
Human
LLM
Agent in team
Who:
When:
What:
How:
Example:
Definition: 
➕
➕
Human
LLM
Agent in team
Who:
When:
What:
How:
Example:
Definition: 
Facilitating
Planning
Users collaborate based on LLM-planned 
tasks, with the LLM allocating tasks 
suited to human or machine capabilities.
Enhancing the LLM agent's understanding 
of human and AI team members' strengths 
enables effective task delegation based on 
their abilities.
Interaction of Thoughts (He et al. 2023)
Users interact with others in team through 
the LLMs facilitation.
Employing an agent within a team to aid in 
communication, information sharing and 
coordination.
Chatbots Facilitating Consensus-Building 
(Shin et al. 2022)
Agent Facilitator
4.
4.2 Capability-aware Task Delegation
4.1 Team Process Facilitating
Human
LLM
Collaborating smoothly via 
LLM agent.
Facilitating team collaboration
Human
LLM
Enhancing human-LLM team 
performance with improved task 
delegation through an agent.
Understanding team member 
capabilities and appropriately 
assigning tasks.
Figure 4: Mode 4: Agent Facilitator. 
knowledge. Further enhancements are possible through structured 
UI design, enabling the establishment of precise characteristics 
under user control, thereby boosting the LLM’s role-play efcacy. 
Similarly, example-based prompting entails providing LLMs with a 
handful of relevant examples that clearly demonstrate the expected 
input and output [76], with the LLM tasked to independently dis­
cern the underlying rationale. 
3.2.4 Mode 4: Agent Facilitator. The agent facilitator mode 
(Figure 4) focuses on enhancing team dynamics and performance 
through LLMs acting as facilitators. 
Mode 4.1. Team Process Facilitating. In this approach, LLMs 
are used to streamline and facilitate the team’s interaction pro­
cess, particularly during the facilitating phase. This is typically 
achieved by integrating an agent within the team that aids in com­
munication [16], decision-making [83], information sharing, and 
coordination. By smoothing out the interaction process, the LLM en­
sures that the team’s workfow continues seamlessly and efectively, 
enhancing collaboration and productivity. 
Mode 4.2. Capability-aware Task Delegation. This approach 
involves augmenting LLMs with the ability to recognize the unique 
capabilities of diferent team members. The primary goal is to lever­
age the diverse skills of team members to optimize overall team 
performance, ensuring that tasks are assigned in a way that maxi­
mizes each member’s contribution and efciency. For instance, in 
response to questions like ‘Can AI perform well?’ [58], the LLM can 
decide whether to assign tasks to each member of a group. This is 
typically crucial during the planning phase and can also be relevant 
in the facilitating phase. 
4 DISCUSSION 
4.1 Two Potential Applications of Interaction 
Modes Taxonomy 
In this paper, we describe a taxonomy specifcally focused on pos­
sible interaction modes between human and LLMs. The goal is to 
empower users to tackle complex tasks by utilizing LLMs beyond 
the default conversational prompting paradigm. Similar to other 
software taxonomies, such as software design patterns [19, 57] and 
catalogs for prompt engineering [69], our taxonomy aims to assist 
software designers in at least two important ways. 
First, by ofering a high-level, systematic, and multi-dimensional 
understanding of interaction modes, this taxonomy empowers 
users to swiftly understand when and how to implement a 
specifc mode, identify the stakeholders involved, and con­
sider relevant factors, thereby enhancing their system design and 
facilitating the evaluation of potential improvements. For instance, 
in brainstorming sessions, users can utilize specifc interaction 
modes from the taxonomy to propose and refne details of their sys­
tem design ideas. Furthermore, after proposing the primary system, 
this taxonomy can serve as a checklist for their designs, prompting 
critical questions such as, "Have I overlooked any crucial steps or 
details?" and "Does my design have any precedents?" 
Second, the taxonomy can unveil new possibilities previ­
ously unconsidered. One approach is through the adoption of 
novel interaction modes that, while initially overlooked, prove to 
be invaluable. For instance, iterating on an established interac­
tion by identifying errors and retrying (Mode 2.4: UI for Testing of 
Iteration), or utilizing an LLM-based agent to enhance team inter­
actions (Mode 4: Agent Facilitator). Additionally, users can discover 
new opportunities by merging elements from various modes, such 
as UI design, reasoning, context, and so on. Several examples in­
clude “human+LLM+role play+UI for input/output" during facilita­
tion; “human+LLM+few-shot examples+UI for input" during facili­
tation; and “human+LLM+explicit constraints+UI for input/output"

A Taxonomy for Human-LLM Interaction Modes: An Initial Exploration 
CHI EA ’24, May 11–16, 2024, Honolulu, HI, USA 
during planning and facilitation. These combinations foster inno­
vative approaches but have not yet been explored in the existing 
research in our reviewing. 
In addition to the ways of applications, we believe our taxon­
omy can be used in many tasks. While the core of our taxonomy– 
prompts–as a form of natural language, initially fnd their primary 
application in writing and coding tasks, we observe their applica­
tion broadening to encompass more tasks that integrate prompts 
into the system’s core. For instance, in the realm of image genera­
tion, although the system’s objective is to produce images, it still 
necessitates natural language prompts as the initiation point. Hence, 
it is plausible to anticipate that the taxonomy of interaction modes 
could serve as a useful tool for designing prompts across various 
domains, such as image and video generation. Overall, our vision 
with this taxonomy is to think of the augmentation of prompts 
of LLMs as a new form of "software" for users to interact with 
hardware and encapsulate data for efcient task execution. 
4.2 Limitations and Future Work 
As highlighted in the title, the taxonomy presented herein repre­
sents an initial endeavor, which we intend to refne continuously. 
We foresee its expansion to encompass additional LLM interaction 
modes likely to emerge in the near future. Moreover, it is important 
to note that many current classifcations in our taxonomy are not 
absolute, given the slight overlap between some categories and the 
potential for misapplication. 
Looking forward, we believe that it will be especially valuable 
to extend the taxonomy to explicitly include diferent kinds of 
tasks and diferent design spaces. For instance, we believe that the 
capabilities and interaction modes needed to creating tasks will 
likely be systematically diferent from the capabilities and modes 
needed to deciding tasks. To do that, we plan to extend our literature 
review to additional venues from diverse felds such as ACL, EMNLP, 
NAACL, TACL, and broader HCI venues like TOCHI, C&C, DIS, 
and even arXiv. 
5 CONCLUSION 
In this paper, we adopt an HCI perspective to explore examine 
interaction modes—patterns we can leverage to enhance LLMs’ 
capabilities through diverse human-LLM interaction designs. Our 
literature review within major HCI venues has led us to identify 
distinct phases of human-LLM interaction fow, and iteratively de­
veloped a taxonomy that encapsulates four key interaction modes 
in human-LLM interaction. This taxonomy provides a valuable tool 
for systematically understanding and analyzing the evolving land­
scape of human-LLM interaction and collaboration. It guides the 
design of human engagement with LLMs in increasingly complex 
and nuanced ways. 
ACKNOWLEDGMENTS 
This research is supported by the National Research Foundation 
(NRF), Prime Minister’s Ofce, Singapore under its Campus for 
Research Excellence and Technological Enterprise (CREATE) pro-
gramme. The Mens, Manus, and Machina (M3S) is an interdisci­
plinary research group (IRG) of the Singapore-MIT Alliance for 
Research and Technology (SMART) centre. 
REFERENCES 
[1] Laura Aina and Tal Linzen. 2021. The language model understood the prompt 
was ambiguous: Probing syntactic uncertainty through generation. arXiv preprint 
arXiv:2109.07848 (2021). 
[2] Tyler Angert, Miroslav Suzara, Jenny Han, Christopher Pondoc, and Hariharan 
Subramonyam. 2023. Spellburst: A Node-based Interface for Exploratory Creative 
Coding with Natural Language Prompts. In Proceedings of the 36th Annual ACM 
Symposium on User Interface Software and Technology. ACM, San Francisco CA 
USA, 1–22. https://doi.org/10.1145/3586183.3606719 
[3] Ian Arawjo, Priyan Vaithilingam, Martin Wattenberg, and Elena Glassman. 2023. 
ChainForge: An open-source visual programming environment for prompt en­
gineering. In Adjunct Proceedings of the 36th Annual ACM Symposium on User 
Interface Software and Technology (UIST ’23 Adjunct). Association for Computing 
Machinery, New York, NY, USA, 1–3. https://doi.org/10.1145/3586182.3616660 
[4] Advait Bhat, Saaket Agashe, Parth Oberoi, Niharika Mohile, Ravi Jangir, and 
Anirudha Joshi. 2023. Interacting with Next-Phrase Suggestions: How Suggestion 
Systems Aid and Infuence the Cognitive Processes of Writing. In Proceedings of 
the 28th International Conference on Intelligent User Interfaces (IUI ’23). Association 
for Computing Machinery, New York, NY, USA, 436–452. https://doi.org/10. 
1145/3581641.3584060 
[5] Michelle Brachman, Qian Pan, Hyo Jin Do, Casey Dugan, Arunima Chaudhary, 
James M. Johnson, Priyanshu Rai, Tathagata Chakraborti, Thomas Gschwind, 
Jim A Laredo, Christoph Miksovic, Paolo Scotton, Kartik Talamadupula, and Gegi 
Thomas. 2023. Follow the Successful Herd: Towards Explanations for Improved 
Use and Mental Models of Natural Language Systems. In Proceedings of the 28th 
International Conference on Intelligent User Interfaces (IUI ’23). Association for 
Computing Machinery, New York, NY, USA, 220–239. https://doi.org/10.1145/ 
3581641.3584088 
[6] Stephen Brade, Bryan Wang, Mauricio Sousa, Sageev Oore, and Tovi Grossman. 
2023. Promptify: Text-to-Image Generation through Interactive Prompt Explo­
ration with Large Language Models. In Proceedings of the 36th Annual ACM 
Symposium on User Interface Software and Technology (UIST ’23). Association 
for Computing Machinery, New York, NY, USA, 1–14. https://doi.org/10.1145/ 
3586183.3606725 
[7] Victor S. Bursztyn, Jennifer Healey, Eunyee Koh, Nedim Lipka, and Larry Birn­
baum. 2021. Developing a Conversational Recommendation System for Navigat­
ing Limited Options. In Extended Abstracts of the 2021 CHI Conference on Human 
Factors in Computing Systems. 1–6. https://doi.org/10.1145/3411763.3451596 
arXiv:2104.06552 [cs]. 
[8] Daniel Buschek, Martin Zürn, and Malin Eiband. 2021. The Impact of Multiple 
Parallel Phrase Suggestions on Email Input and Composition Behaviour of Native 
and Non-Native English Writers. In Proceedings of the 2021 CHI Conference on 
Human Factors in Computing Systems. ACM, Yokohama Japan, 1–13. https: 
//doi.org/10.1145/3411764.3445372 
[9] Yuzhe Cai, Shaoguang Mao, Wenshan Wu, Zehua Wang, Yaobo Liang, Tao Ge, 
Chenfei Wu, Wang You, Ting Song, Yan Xia, Jonathan Tien, and Nan Duan. 2023. 
Low-code LLM: Visual Programming over LLMs. arXiv:2304.08103 [cs.CL] 
[10] Weihao Chen, Chun Yu, Huadong Wang, Zheng Wang, Lichen Yang, Yukun Wang, 
Weinan Shi, and Yuanchun Shi. 2023. From Gap to Synergy: Enhancing Contextual 
Understanding through Human-Machine Collaboration in Personalized Systems. 
In Proceedings of the 36th Annual ACM Symposium on User Interface Software 
and Technology (UIST ’23). Association for Computing Machinery, New York, NY, 
USA, 1–15. https://doi.org/10.1145/3586183.3606741 
[11] John Joon Young Chung, Wooseok Kim, Kang Min Yoo, Hwaran Lee, Eytan 
Adar, and Minsuk Chang. 2022. TaleBrush: Sketching Stories with Generative 
Pretrained Language Models. In CHI Conference on Human Factors in Computing 
Systems. ACM, New Orleans LA USA, 1–19. https://doi.org/10.1145/3491102. 
3501819 
[12] Andrea Cuadra, Shuran Li, Hansol Lee, Jason Cho, and Wendy Ju. 2021. My Bad! 
Repairing Intelligent Voice Assistant Errors Improves Interaction. Proceedings 
of the ACM on Human-Computer Interaction 5, CSCW1 (April 2021), 27:1–27:24. 
https://doi.org/10.1145/3449101 
[13] Hai Dang, Karim Benharrak, Florian Lehmann, and Daniel Buschek. 2022. Beyond 
Text Generation: Supporting Writers with Continuous Automatic Text Summaries. 
In Proceedings of the 35th Annual ACM Symposium on User Interface Software 
and Technology (UIST ’22). Association for Computing Machinery, New York, NY, 
USA, 1–13. https://doi.org/10.1145/3526113.3545672 
[14] Hai Dang, Sven Goller, Florian Lehmann, and Daniel Buschek. 2023. Choice 
Over Control: How Users Write with Large Language Models using Diegetic and 
Non-Diegetic Prompting. In Proceedings of the 2023 CHI Conference on Human 
Factors in Computing Systems. ACM, Hamburg Germany, 1–17. https://doi.org/ 
10.1145/3544548.3580969 
[15] Hai Dang, Lukas Mecke, Florian Lehmann, Sven Goller, and Daniel Buschek. 2022. 
How to Prompt? Opportunities and Challenges of Zero- and Few-Shot Learning 
for Human-AI Interaction in Creative Applications of Generative Models. http: 
//arxiv.org/abs/2209.01390 arXiv:2209.01390 [cs].

CHI EA ’24, May 11–16, 2024, Honolulu, HI, USA 
Jie Gao, Simret Araya Gebreegziabher et al. 
[16] Wen Duan, Naomi Yamashita, Yoshinari Shirai, and Susan R. Fussell. 2021. 
Bridging Fluency Disparity between Native and Nonnative Speakers in Mul­
tilingual Multiparty Collaboration Using a Clarifcation Agent. Proceedings of 
the ACM on Human-Computer Interaction 5, CSCW2 (Oct. 2021), 435:1–435:31. 
https://doi.org/10.1145/3479579 
[17] Noyan Evirgen and Xiang ’Anthony’ Chen. 2022. GANzilla: User-Driven Direction 
Discovery in Generative Adversarial Networks. In Proceedings of the 35th Annual 
ACM Symposium on User Interface Software and Technology. ACM, Bend OR USA, 
1–10. https://doi.org/10.1145/3526113.3545638 
[18] Mingming Fan, Xianyou Yang, TszTung Yu, Q. Vera Liao, and Jian Zhao. 2022. 
Human-AI Collaboration for UX Evaluation: Efects of Explanation and Synchro­
nization. Proceedings of the ACM on Human-Computer Interaction 6, CSCW1 
(April 2022), 96:1–96:32. https://doi.org/10.1145/3512943 
[19] Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides. 1995. Design 
patterns: elements of reusable object-oriented software. Addison-Wesley Longman 
Publishing Co., Inc., USA. 
[20] Simret Araya Gebreegziabher, Zheng Zhang, Xiaohang Tang, Yihao Meng, Elena L. 
Glassman, and Toby Jia-Jun Li. 2023. PaTAT: Human-AI Collaborative Qualitative 
Coding with Explainable Interactive Rule Synthesis. In Proceedings of the 2023 CHI 
Conference on Human Factors in Computing Systems. ACM, Hamburg Germany, 
1–19. https://doi.org/10.1145/3544548.3581352 
[21] Hongyan Gu, Chunxu Yang, Mohammad Haeri, Jing Wang, Shirley Tang, Wen­
zhong Yan, Shujin He, Christopher Kazu Williams, Shino Magaki, and Xiang ’An­
thony’ Chen. 2023. Augmenting Pathologists with NaviPath: Design and Eval­
uation of a Human-AI Collaborative Navigation System. In Proceedings of the 
2023 CHI Conference on Human Factors in Computing Systems. ACM, Hamburg 
Germany, 1–19. https://doi.org/10.1145/3544548.3580694 
[22] Ziyao He, Yunpeng Song, Shurui Zhou, and Zhongmin Cai. 2023. Interaction 
of Thoughts: Towards Mediating Task Assignment in Human-AI Cooperation 
with a Capability-Aware Shared Mental Model. In Proceedings of the 2023 CHI 
Conference on Human Factors in Computing Systems. ACM, Hamburg Germany, 
1–18. https://doi.org/10.1145/3544548.3580983 
[23] Takumi Ito, Naomi Yamashita, Tatsuki Kuribayashi, Masatoshi Hidaka, Jun Suzuki, 
Ge Gao, Jack Jamieson, and Kentaro Inui. 2023. Use of an AI-powered Rewriting 
Support Software in Context with Other Tools: A Study of Non-Native English 
Speakers. In Proceedings of the 36th Annual ACM Symposium on User Interface 
Software and Technology (UIST ’23). Association for Computing Machinery, New 
York, NY, USA, 1–13. https://doi.org/10.1145/3586183.3606810 
[24] Ellen Jiang, Kristen Olson, Edwin Toh, Alejandra Molina, Aaron Donsbach, 
Michael Terry, and Carrie J Cai. 2022. PromptMaker: Prompt-based Proto­
typing with Large Language Models. In CHI Conference on Human Factors 
in Computing Systems Extended Abstracts. ACM, New Orleans LA USA, 1–8. 
https://doi.org/10.1145/3491101.3503564 
[25] Ellen Jiang, Edwin Toh, Alejandra Molina, Aaron Donsbach, Carrie J Cai, and 
Michael Terry. 2021. GenLine and GenForm: Two Tools for Interacting with 
Generative Language Models in a Code Editor. In Adjunct Proceedings of the 34th 
Annual ACM Symposium on User Interface Software and Technology. ACM, Virtual 
Event USA, 145–147. https://doi.org/10.1145/3474349.3480209 
[26] Ellen Jiang, Edwin Toh, Alejandra Molina, Kristen Olson, Claire Kayacik, Aaron 
Donsbach, Carrie J Cai, and Michael Terry. 2022. Discovering the Syntax and 
Strategies of Natural Language Programming with Generative Language Models. 
In CHI Conference on Human Factors in Computing Systems. ACM, New Orleans 
LA USA, 1–19. https://doi.org/10.1145/3491102.3501870 
[27] Peiling Jiang, Jude Rayan, Steven P Dow, and Haijun Xia. 2023. Graphologue: 
Exploring Large Language Model Responses with Interactive Diagrams. arXiv 
preprint arXiv:2305.11473 (2023). 
[28] Peiling Jiang, Jude Rayan, Steven P. Dow, and Haijun Xia. 2023. Graphologue: 
Exploring Large Language Model Responses with Interactive Diagrams. In Pro­
ceedings of the 36th Annual ACM Symposium on User Interface Software and 
Technology (UIST ’23). Association for Computing Machinery, New York, NY, 
USA, 1–20. https://doi.org/10.1145/3586183.3606737 
[29] Eunkyung Jo, Daniel A. Epstein, Hyunhoon Jung, and Young-Ho Kim. 2023. 
Understanding the Benefts and Challenges of Deploying Conversational AI 
Leveraging Large Language Models for Public Health Intervention. In Proceed­
ings of the 2023 CHI Conference on Human Factors in Computing Systems. ACM, 
Hamburg Germany, 1–16. https://doi.org/10.1145/3544548.3581503 
[30] Hyunggu Jung, Woosuk Seo, Seokwoo Song, and Sungmin Na. 2023. Toward 
Value Scenario Generation Through Large Language Models. In Companion 
Publication of the 2023 Conference on Computer Supported Cooperative Work and 
Social Computing (CSCW ’23 Companion). Association for Computing Machinery, 
New York, NY, USA, 212–220. https://doi.org/10.1145/3584931.3606960 
[31] Jeesu Jung, Hyein Seo, Sangkeun Jung, Riwoo Chung, Hwijung Ryu, and Du-
Seong Chang. 2023. Interactive User Interface for Dialogue Summarization. 
In Proceedings of the 28th International Conference on Intelligent User Interfaces 
(IUI ’23). Association for Computing Machinery, New York, NY, USA, 934–957. 
https://doi.org/10.1145/3581641.3584057 
[32] Stafs Keele et al. 2007. Guidelines for performing systematic literature reviews 
in software engineering. 
[33] Taewook Kim, Qingyu Guo, Hyeonjae Kim, Wenjie Yang, Meiziniu Li, and Xi­
aojuan Ma. 2022. Facilitating Continuous Text Messaging in Online Romantic 
Encounters by Expanded Keywords Enumeration. In Companion Publication of 
the 2022 Conference on Computer Supported Cooperative Work and Social Comput­
ing (CSCW’22 Companion). Association for Computing Machinery, New York, 
NY, USA, 3–7. https://doi.org/10.1145/3500868.3559441 
[34] Tae Soo Kim, DaEun Choi, Yoonseo Choi, and Juho Kim. 2022. Stylette: Styling the 
Web with Natural Language. In CHI Conference on Human Factors in Computing 
Systems. ACM, New Orleans LA USA, 1–17. https://doi.org/10.1145/3491102. 
3501931 
[35] Tae Soo Kim, Yoonjoo Lee, Minsuk Chang, and Juho Kim. 2023. Cells, Generators, 
and Lenses: Design Framework for Object-Oriented Interaction with Large Lan­
guage Models. In Proceedings of the 36th Annual ACM Symposium on User Interface 
Software and Technology (UIST ’23). Association for Computing Machinery, New 
York, NY, USA, 1–18. https://doi.org/10.1145/3586183.3606833 
[36] Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, and Yusuke 
Iwasawa. 2022. Large language models are zero-shot reasoners. Advances in 
neural information processing systems 35 (2022), 22199–22213. 
[37] Harsh Kumar, Yiyi Wang, Jiakai Shi, Ilya Musabirov, Norman A. S. Farb, and 
Joseph Jay Williams. 2023. Exploring the Use of Large Language Models for 
Improving the Awareness of Mindfulness. In Extended Abstracts of the 2023 CHI 
Conference on Human Factors in Computing Systems. ACM, Hamburg Germany, 
1–7. https://doi.org/10.1145/3544549.3585614 
[38] Vivian Lai, Samuel Carton, Rajat Bhatnagar, Q. Vera Liao, Yunfeng Zhang, and 
Chenhao Tan. 2022. Human-AI Collaboration via Conditional Delegation: A Case 
Study of Content Moderation. http://arxiv.org/abs/2204.11788 arXiv:2204.11788 
[cs]. 
[39] Ray Lc and Daijiro Mizuno. 2021. Designing for Narrative Infuence:: Speculative 
Storytelling for Social Good in Times of Public Health and Climate Crises. In 
Extended Abstracts of the 2021 CHI Conference on Human Factors in Computing 
Systems. ACM, Yokohama Japan, 1–13. https://doi.org/10.1145/3411763.3450373 
[40] Mina Lee, Percy Liang, and Qian Yang. 2022. CoAuthor: Designing a Human-AI 
Collaborative Writing Dataset for Exploring Language Model Capabilities. In 
CHI Conference on Human Factors in Computing Systems. 1–19. https://doi.org/ 
10.1145/3491102.3502030 arXiv:2201.06796 [cs]. 
[41] Yi-Chieh Lee, Naomi Yamashita, and Yun Huang. 2021. Exploring the Efects of 
Incorporating Human Experts to Deliver Journaling Guidance through a Chatbot. 
Proceedings of the ACM on Human-Computer Interaction 5, CSCW1 (April 2021), 
122:1–122:27. https://doi.org/10.1145/3449196 
[42] Stephan J Lemmer, Anhong Guo, and Jason J Corso. 2023. Human-Centered 
Deferred Inference: Measuring User Interactions and Setting Deferral Criteria for 
Human-AI Teams. In Proceedings of the 28th International Conference on Intelligent 
User Interfaces (IUI ’23). Association for Computing Machinery, New York, NY, 
USA, 681–694. https://doi.org/10.1145/3581641.3584092 
[43] Michael Xieyang Liu, Advait Sarkar, Carina Negreanu, Benjamin Zorn, Jack 
Williams, Neil Toronto, and Andrew D. Gordon. 2023. “What It Wants Me To 
Say”: Bridging the Abstraction Gap Between End-User Programmers and Code-
Generating Large Language Models. In Proceedings of the 2023 CHI Conference on 
Human Factors in Computing Systems. ACM, Hamburg Germany, 1–31. https: 
//doi.org/10.1145/3544548.3580817 
[44] Vivian Liu, Han Qiao, and Lydia Chilton. 2022. Opal: Multimodal Image Gen­
eration for News Illustration. In Proceedings of the 35th Annual ACM Sympo­
sium on User Interface Software and Technology. ACM, Bend OR USA, 1–17. 
https://doi.org/10.1145/3526113.3545621 
[45] Robert L Logan IV, Ivana Balažević, Eric Wallace, Fabio Petroni, Sameer Singh, 
and Sebastian Riedel. 2021. Cutting down on prompts and parameters: Simple 
few-shot learning with language models. arXiv preprint arXiv:2106.13353 (2021). 
[46] Ryan Louie, Jesse Engel, and Cheng-Zhi Anna Huang. 2022. Expressive Commu­
nication: Evaluating Developments in Generative Models and Steering Interfaces 
for Music Creation. In 27th International Conference on Intelligent User Interfaces 
(IUI ’22). Association for Computing Machinery, New York, NY, USA, 405–417. 
https://doi.org/10.1145/3490099.3511159 
[47] Andrew M Mcnutt, Chenglong Wang, Robert A Deline, and Steven M. Drucker. 
2023. On the Design of AI-powered Code Assistants for Notebooks. In Proceed­
ings of the 2023 CHI Conference on Human Factors in Computing Systems. ACM, 
Hamburg Germany, 1–16. https://doi.org/10.1145/3544548.3580940 
[48] Piotr Mirowski, Kory W. Mathewson, Jaylen Pittman, and Richard Evans. 2023. 
Co-Writing Screenplays and Theatre Scripts with Language Models: Evaluation 
by Industry Professionals. In Proceedings of the 2023 CHI Conference on Human 
Factors in Computing Systems. ACM, Hamburg Germany, 1–34. https://doi.org/ 
10.1145/3544548.3581225 
[49] Anwesha Mukherjee, Vagner Figueredo De Santana, and Alexis Baria. 2023. 
ImpactBot: Chatbot Leveraging Language Models to Automate Feedback and 
Promote Critical Thinking Around Impact Statements. In Extended Abstracts of 
the 2023 CHI Conference on Human Factors in Computing Systems. ACM, Hamburg 
Germany, 1–8. https://doi.org/10.1145/3544549.3573844 
[50] Arpit Narechania, Adam Fourney, Bongshin Lee, and Gonzalo Ramos. 2021. 
DIY: Assessing the Correctness of Natural Language to SQL Systems. In 26th

A Taxonomy for Human-LLM Interaction Modes: An Initial Exploration 
CHI EA ’24, May 11–16, 2024, Honolulu, HI, USA 
International Conference on Intelligent User Interfaces (IUI ’21). Association for 
Computing Machinery, New York, NY, USA, 597–607. https://doi.org/10.1145/ 
3397481.3450667 
[51] Hiroyuki Osone, Jun-Li Lu, and Yoichi Ochiai. 2021. BunCho: AI Supported Story 
Co-Creation via Unsupervised Multitask Learning to Increase Writers’ Creativity 
in Japanese. In Extended Abstracts of the 2021 CHI Conference on Human Factors 
in Computing Systems. ACM, Yokohama Japan, 1–10. https://doi.org/10.1145/ 
3411763.3450391 
[52] Savvas Petridis, Michael Terry, and Carrie Jun Cai. 2023. PromptInfuser: Bring­
ing User Interface Mock-ups to Life with Large Language Models. In Extended 
Abstracts of the 2023 CHI Conference on Human Factors in Computing Systems. 
ACM, Hamburg Germany, 1–6. https://doi.org/10.1145/3544549.3585628 
[53] Kevin Pu, Rainey Fu, Rui Dong, Xinyu Wang, Yan Chen, and Tovi Grossman. 
2022. SemanticOn: Specifying Content-Based Semantic Conditions for Web 
Automation Programs. In Proceedings of the 35th Annual ACM Symposium on 
User Interface Software and Technology. ACM, Bend OR USA, 1–16. https://doi. 
org/10.1145/3526113.3545691 
[54] Aditya kumar Purohit, Aditya Upadhyaya, and Adrian Holzer. 2023. ChatGPT in 
Healthcare: Exploring AI Chatbot for Spontaneous Word Retrieval in Aphasia. In 
Companion Publication of the 2023 Conference on Computer Supported Cooperative 
Work and Social Computing (CSCW ’23 Companion). Association for Computing 
Machinery, New York, NY, USA, 1–5. https://doi.org/10.1145/3584931.3606993 
[55] Laria Reynolds and Kyle McDonell. 2021. Prompt Programming for Large Lan­
guage Models: Beyond the Few-Shot Paradigm. In Extended Abstracts of the 2021 
CHI Conference on Human Factors in Computing Systems. ACM, Yokohama Japan, 
1–7. https://doi.org/10.1145/3411763.3451760 
[56] Steven I. Ross, Fernando Martinez, Stephanie Houde, Michael Muller, and Justin D. 
Weisz. 2023. The Programmer’s Assistant: Conversational Interaction with a 
Large Language Model for Software Development. In Proceedings of the 28th 
International Conference on Intelligent User Interfaces (IUI ’23). Association for 
Computing Machinery, New York, NY, USA, 491–514. https://doi.org/10.1145/ 
3581641.3584037 
[57] Douglas C Schmidt, Michael Stal, Hans Rohnert, and Frank Buschmann. 2013. 
Pattern-oriented software architecture, patterns for concurrent and networked objects. 
John Wiley & Sons. 
[58] Chuhan Shi, Yicheng Hu, Shenan Wang, Shuai Ma, Chengbo Zheng, Xiaojuan Ma, 
and Qiong Luo. 2023. RetroLens: A Human-AI Collaborative System for Multi-
step Retrosynthetic Route Planning. In Proceedings of the 2023 CHI Conference on 
Human Factors in Computing Systems. ACM, Hamburg Germany, 1–20. https: 
//doi.org/10.1145/3544548.3581469 
[59] Joongi Shin, Michael A. Hedderich, AndréS Lucero, and Antti Oulasvirta. 2022. 
Chatbots Facilitating Consensus-Building in Asynchronous Co-Design. In Pro­
ceedings of the 35th Annual ACM Symposium on User Interface Software and 
Technology (UIST ’22). Association for Computing Machinery, New York, NY, 
USA, 1–13. https://doi.org/10.1145/3526113.3545671 
[60] Ben Shneiderman and Catherine Plaisant. 2004. Designing the User Interface: 
Strategies for Efective Human-Computer Interaction (4th Edition). Pearson Addison 
Wesley. 
[61] Sruti Srinivasa Ragavan, Zhitao Hou, Yun Wang, Andrew D Gordon, Haidong 
Zhang, and Dongmei Zhang. 2022. GridBook: Natural Language Formulas for the 
Spreadsheet Grid. In 27th International Conference on Intelligent User Interfaces 
(IUI ’22). Association for Computing Machinery, New York, NY, USA, 345–368. 
https://doi.org/10.1145/3490099.3511161 
[62] Arjun Srinivasan and Vidya Setlur. 2021. Snowy: Recommending Utterances for 
Conversational Visual Analysis. In The 34th Annual ACM Symposium on User In­
terface Software and Technology (UIST ’21). Association for Computing Machinery, 
New York, NY, USA, 864–880. https://doi.org/10.1145/3472749.3474792 
[63] Sangho Suh, Bryan Min, Srishti Palani, and Haijun Xia. 2023. Sensecape: En­
abling Multilevel Exploration and Sensemaking with Large Language Models. 
arXiv:2305.11483 [cs.HC] 
[64] Sangho Suh, Bryan Min, Srishti Palani, and Haijun Xia. 2023. Sensecape: En­
abling Multilevel Exploration and Sensemaking with Large Language Models. 
In Proceedings of the 36th Annual ACM Symposium on User Interface Software 
and Technology (UIST ’23). Association for Computing Machinery, New York, NY, 
USA, 1–18. https://doi.org/10.1145/3586183.3606756 
[65] Bryan Wang, Gang Li, and Yang Li. 2023. Enabling Conversational Interaction 
with Mobile UI Using Large Language Models. In Proceedings of the 2023 CHI 
Conference on Human Factors in Computing Systems (Hamburg, Germany) (CHI 
’23). Association for Computing Machinery, New York, NY, USA, Article 432, 
17 pages. https://doi.org/10.1145/3544548.3580895 
[66] Sitong Wang, Savvas Petridis, Taeahn Kwon, Xiaojuan Ma, and Lydia B Chilton. 
2023. PopBlends: Strategies for Conceptual Blending with Large Language Models. 
In Proceedings of the 2023 CHI Conference on Human Factors in Computing Systems. 
ACM, Hamburg Germany, 1–19. https://doi.org/10.1145/3544548.3580948 
[67] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, 
Ed Chi, Quoc Le, and Denny Zhou. 2023. Chain-of-Thought Prompting Elicits 
Reasoning in Large Language Models. arXiv:2201.11903 [cs.CL] 
[68] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, 
Quoc V Le, Denny Zhou, et al. 2022. Chain-of-thought prompting elicits reasoning 
in large language models. Advances in Neural Information Processing Systems 35 
(2022), 24824–24837. 
[69] Jules White, Quchen Fu, Sam Hays, Michael Sandborn, Carlos Olea, Henry 
Gilbert, Ashraf Elnashar, Jesse Spencer-Smith, and Douglas C. Schmidt. 2023. 
A Prompt Pattern Catalog to Enhance Prompt Engineering with ChatGPT. 
arXiv:2302.11382 [cs.SE] 
[70] Sherry Wu, Hua Shen, Daniel S Weld, Jefrey Heer, and Marco Tulio Ribeiro. 2023. 
ScatterShot: Interactive In-context Example Curation for Text Transformation. 
In Proceedings of the 28th International Conference on Intelligent User Interfaces 
(IUI ’23). Association for Computing Machinery, New York, NY, USA, 353–367. 
https://doi.org/10.1145/3581641.3584059 
[71] Tongshuang Wu, Ellen Jiang, Aaron Donsbach, Jef Gray, Alejandra Molina, 
Michael Terry, and Carrie J. Cai. 2022. PromptChainer: Chaining Large Language 
Model Prompts through Visual Programming. http://arxiv.org/abs/2203.06566 
arXiv:2203.06566 [cs]. 
[72] Tongshuang Wu, Michael Terry, and Carrie Jun Cai. 2022. AI Chains: Transparent 
and Controllable Human-AI Interaction by Chaining Large Language Model 
Prompts. In CHI Conference on Human Factors in Computing Systems. ACM, New 
Orleans LA USA, 1–22. https://doi.org/10.1145/3491102.3517582 
[73] Tongshuang Wu, Michael Terry, and Carrie J. Cai. 2022. AI Chains: Transparent 
and Controllable Human-AI Interaction by Chaining Large Language Model 
Prompts. arXiv:2110.01691 [cs.HC] 
[74] Chang Xiao. 2023. AutoSurveyGPT: GPT-Enhanced Automated Literature Discov­
ery. In Adjunct Proceedings of the 36th Annual ACM Symposium on User Interface 
Software and Technology (UIST ’23 Adjunct). Association for Computing Machin­
ery, New York, NY, USA, 1–3. https://doi.org/10.1145/3586182.3616648 
[75] Ziang Xiao, Sarah Mennicken, Bernd Huber, Adam Shonkof, and Jennifer Thom. 
2021. Let Me Ask You This: How Can a Voice Assistant Elicit Explicit User 
Feedback? Proceedings of the ACM on Human-Computer Interaction 5, CSCW2 
(Oct. 2021), 388:1–388:24. https://doi.org/10.1145/3479532 
[76] Ziang Xiao, Xingdi Yuan, Q. Vera Liao, Rania Abdelghani, and Pierre-Yves 
Oudeyer. 2023. Supporting Qualitative Analysis with Large Language Models: 
Combining Codebook with GPT-3 for Deductive Coding. In 28th International 
Conference on Intelligent User Interfaces. ACM, Sydney NSW Australia, 75–78. 
https://doi.org/10.1145/3581754.3584136 
[77] Ann Yuan, Andy Coenen, Emily Reif, and Daphne Ippolito. 2022. Wordcraft: 
Story Writing With Large Language Models. In 27th International Conference on 
Intelligent User Interfaces (IUI ’22). Association for Computing Machinery, New 
York, NY, USA, 841–852. https://doi.org/10.1145/3490099.3511105 
[78] J.D. Zamfrescu-Pereira, Richmond Y. Wong, Bjoern Hartmann, and Qian Yang. 
2023. Why Johnny Can’t Prompt: How Non-AI Experts Try (and Fail) to Design 
LLM Prompts. In Proceedings of the 2023 CHI Conference on Human Factors in 
Computing Systems. ACM, Hamburg Germany, 1–21. https://doi.org/10.1145/ 
3544548.3581388 
[79] Mingyuan Zhang, Zhaolin Cheng, Sheung Ting Ramona Shiu, Jiacheng Liang, 
Cong Fang, Zhengtao Ma, Le Fang, and Stephen Jia Wang. 2023. Towards Human-
Centred AI-Co-Creation: A Three-Level Framework for Efective Collaboration 
between Human and AI. In Companion Publication of the 2023 Conference on 
Computer Supported Cooperative Work and Social Computing (CSCW ’23 Com­
panion). Association for Computing Machinery, New York, NY, USA, 312–316. 
https://doi.org/10.1145/3584931.3607008 
[80] Zheng Zhang, Jie Gao, Ranjodh Singh Dhaliwal, and Toby Jia-Jun Li. 2023. VISAR: 
A Human-AI Argumentative Writing Assistant with Visual Programming and 
Rapid Draft Prototyping. arXiv preprint arXiv:2304.07810 (2023). 
[81] Zheng Zhang, Ying Xu, Yanhao Wang, Bingsheng Yao, Daniel Ritchie, Tong­
shuang Wu, Mo Yu, Dakuo Wang, and Toby Jia-Jun Li. 2022. StoryBuddy: A 
Human-AI Collaborative Chatbot for Parent-Child Interactive Storytelling with 
Flexible Parental Involvement. In CHI Conference on Human Factors in Computing 
Systems. ACM, New Orleans LA USA, 1–21. https://doi.org/10.1145/3491102. 
3517479 
[82] Yubo Zhao and Xiying Bao. 2023. Narratron: Collaborative Writing and Shadow-
playing of Children Stories with Large Language Models. In Adjunct Proceedings 
of the 36th Annual ACM Symposium on User Interface Software and Technology. 
ACM, San Francisco CA USA, 1–6. https://doi.org/10.1145/3586182.3625120 
[83] Chengbo Zheng, Yuheng Wu, Chuhan Shi, Shuai Ma, Jiehui Luo, and Xiaojuan 
Ma. 2023. Competent but Rigid: Identifying the Gap in Empowering AI to 
Participate Equally in Group Decision-Making. In Proceedings of the 2023 CHI 
Conference on Human Factors in Computing Systems. ACM, Hamburg Germany, 
1–19. https://doi.org/10.1145/3544548.3581131 
[84] Yijun Zhou, Yuki Koyama, Masataka Goto, and Takeo Igarashi. 2021. Interactive 
Exploration-Exploitation Balancing for Generative Melody Composition. In 26th 
International Conference on Intelligent User Interfaces (IUI ’21). Association for 
Computing Machinery, New York, NY, USA, 43–47. https://doi.org/10.1145/ 
3397481.3450663

CHI EA ’24, May 11–16, 2024, Honolulu, HI, USA 
Jie Gao, Simret Araya Gebreegziabher et al. 
[85] Qingxiaoyang Zhu and Hao-Chuan Wang. 2023. Leveraging Large Language 
Model as Support for Human Problem Solving: An Exploration of Its Appro­
priation and Impact. In Companion Publication of the 2023 Conference on Com­
puter Supported Cooperative Work and Social Computing (CSCW ’23 Compan­
ion). Association for Computing Machinery, New York, NY, USA, 333–337. 
https://doi.org/10.1145/3584931.3606965

A Taxonomy for Human-LLM Interaction Modes: An Initial Exploration 
CHI EA ’24, May 11–16, 2024, Honolulu, HI, USA 
Table 2: The table shows all the papers included in the taxonomy. 
Taxonomy 
Subcatagory 
Citations 
[85] [30] [56] [29] 
Mode 1. Standard Prompting 
Mode 1.1. Text-based Conversational Prompting 
[40] [81] [39] [75] 
[7] [55] [8] [49] 
Mode 1.2. Text-based Conversational Prompting with Reasoning 
[73] [42] 
[33] [44] [2][46] 
Mode 2.1. UI for Structured Input 
[14] [66] [15] [24] 
[51] 
Mode 2. User Interface (UI) 
[25] [23] [4] [77] 
Mode 2.2. UI for Varying Output 
[50] [84] [47] [20] 
[52] [26] [34] [11] 
[5] [48] 
Mode 2.3. UI for Iteration of Interaction 
[12] [82] [6] [13] 
[31] [21] [43] [78] 
Mode 2.4. UI for Testing of Interaction 
[35] [80] [17] 
Mode 2.5. UI for Reasoning 
[79] [71] [28] [64] 
[3] [65] 
Mode 3. Context-based 
Mode 3.1. Explicit Context 
Mode 3.2. Implicit Context 
[74] [53] [70] [76] 
[10] [62] [37] [61] 
[76] [18] 
Mode 4. Agent Facilitator 
Mode 4.1. Team process facilitating 
[16] [59] [83] [54] 
Mode 4.2. Capability-aware Task Delegation 
[41] [22] [58] [38] 
Table 3: The primary version of taxonomy in Section 2.2.1. 
Interaction Modes 
Who 
When 
Wow 
Defnition 
Example 
UI+prompts 
User, 
LLMs+UI 
Proposing 
Consistent and comprehensive 
input prompts 
Using an interface design to structure 
the input of zero-shot, few-shot. Propose 
interface that supports the prompts to 
be step-by-step evolved/organize 
prompts/input prompts structurely 
Design customized UI to get customized prompts: 
(1) Complete the sentence. 
(2) Complete the sentence and <user_instruction>. 
Structured interface that allows users to input 
few-shot examples consistently 
Iteration 
More rounds of prompting, 
for refection and improvement 
of the quality 
Iteration of the prompting /conversational 
process: (1) allows users to create an 
LLM-based chatbot solely through prompts, 
and (2) encourages iterative design and 
evaluation of efective prompt strategies. 
1. Defning a “baseline” chatbot prompt template 
2. Assessing what the baseline bot is capable of 
3. Identifying errors. 
4. Debugging 
5. Evaluating the new prompt locally. 
6. Evaluating the new prompt globally. 
7. Iteration. 
Conversational and 
Step-by-step 
User, 
LLMs+reasoning 
Proposing 
Iteration 
Improve prompt quality, 
iterate the results 
Human gives input and get several intermediate 
results from LLMs and then do editing/give 
feedback to iterate the results 
Low-codeLLM: VisualProgramming overLLMs: 
“What It Wants Me To Say”: Bridging the 
Abstraction Gap Between End-User Programmers 
and Code-Generating Large Language Models 
Proposing 
Acomplish reasoning on 
complex tasks. 
For complex reasoning tasks, split the 
tasks into subtasks. 
Chain of thought, Self-Consistency, 
Automatic Reasoning and Tool-use (ART). 
Decomposed Prompting : A MODULAR 
APPROACH FOR SOLVING COMPLEX TASKS 
Role Play 
User, 
LLMs+role/persona 
Proposing 
Get responses like some 
pre-defned persona, 
improve the quality of results 
Setting the characteristics/role/persona 
e.g., Ask GPT to act as a proofreader 
Context based 
User, 
LLMs + context 
Proposing 
Drive responses into 
specifc directions 
Ask GPT to generate outputs from 
diferent dimensions 
deductive/inductive, 
example-centered/codebook-centered
