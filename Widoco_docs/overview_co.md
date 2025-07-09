# Climate Ontology Description
This is an excerpt from a paper, hence the figures start at 5.

Our current model of Climate Obstruction integrates three different models [3], [4], and [5]. These models share ideas, but they were not designed to be part of one coherent model. In addition to providing a tool for climate obstruction researchers, an additional (and ultimately more important) goal of this project is to show how the Neurosymbolic architecture can provide a formal foundation for theories, leading to theories in the social science that make falsifiable predictions. Each of those sources emphasize different aspects of Climate Obstruction: Modeling Influence flow, modeling Greenwashing, and modeling Field Frames. We will discuss each of the different models and how we formalized and integrated them. 
## Influence Flows
![image](https://github.com/user-attachments/assets/5e5b9caa-a58b-4fbc-a4ef-d5f018ab1eaa)

**Figure 5**. Figure 1 from: [Climate Obstruction in Europe](https://cssn.org/news-research/europe-volume/) Used with Permission.

The model in [4] is based on a graph of the way influence flows across stake holders in the Climate Obstruction network. The graph for that model (reused with kind permission from Robert Brulle) is shown in Fig. 5. The first obvious characteristic of this model is that it is a meta-model. I.e., a model of classes and the flows between them. As a result, our first approach was to model the nodes in Fig. 5 as punned classes. However, on closer inspection, this wasn’t adequate. When we record things such as a funding donation from one Agent to another we want to include data such as the date of the donation, the receiver, the giver, the amount, etc. Thus, rather than modeling the edges in Fig. 5 as object properties, we needed to reify the relations. We decided that the Event class (shared across both Gist and the UMG) was the proper way to model influence flows. I.e., funding donations, testimony at hearings, support for political agendas are all examples of Events. This was an especially good fit for Gist as it emphasizes concepts such as contracts and transactions. At first we made the class Influence Event a subclass of Communication Event. On closer inspection some of the edges in Fig. 5 involve more than communication (e.g., Political Mobilization). This is where multiple inheritance can be useful. Using multiple inheritance, we were able to preserve the model defined in Fig. 5 where each edge is a subclass of Influence Event and most, but not all of those classes are also subclasses of Communication Event. Fig. 6 shows the Influence Event hierarchy within the context of the ontology in Protégé. 

![image](https://github.com/user-attachments/assets/ba978bf6-7fac-4e00-9ca3-61f9ecacae67)


**Figure 6**. Influence Event Classes

We model most of the nodes in Fig. 5 as Agent subclasses. Gist doesn’t use the Agent pattern that is common in many ontologies such as FOAF and Prov-O as well as the UMG ontology. The core idea across all these models is that there are many processes and data that apply both to a Person and an Organization. They can both sign contracts, be assigned moral responsibility, have emails, have physical addresses, execute tasks, etc. The various connections in Fig. 5 are modeled as axioms on each class as shown in Fig. 6. In addition, we used the model of causality in the UMG as well as Gist properties such as giver, receiver, comes from agent, etc. to model the various properties required to completely define the graph in Fig. 5 that indicate the path of influence starting from corporate donations and resulting in political outcomes. Using a property hierarchy (see Fig. 7) allows us to model various kinds of influence relations such as funding and publication, while at the same time recording that all these properties are different ways to causally influence other parts of the model. The top property takes the transitive closure of all causal relations. This allows us to visualize causal flows from corporate donations, to disinformation, and ultimately to political outcomes as shown in Fig. 11.

![image](https://github.com/user-attachments/assets/9065d1e5-4238-4d5c-a190-b3309114900e)
**Figure 7**. Causal property hierarchy

# Greenwashing

![image](https://github.com/user-attachments/assets/628c7c04-3ca2-4b1a-a265-a8626c196453)
**Figure 8**. Greenwashing classes

The model in [5] defines a taxonomy of types of green washing. This is straight forward as all types of Green Washing are some type of Communication Event. Hence, the Green Washing model fit naturally under our Communication Event class as shown in Fig. 8.
# Field Frames
Finally, we integrated the model in [3]. This model is built on the concept of a Field Frame which Brulle reused from previous work by other social scientists. Brulle defines a field frame as: “a shared perspective of the situation. [that] forms a taken-for-granted reality and defines norms for regularized patterns of social interaction” [3]. This definition was a natural fit to the concept of a Belief and a Belief System from the UMG. A Belief is holding one or more propositions to be true. We model a Proposition as a reified triple. This enables us to model the fact that different groups and individuals may believe propositions that are logically incompatible with each other without causing the ontology to be inconsistent. A Belief System is a collection of one or more Beliefs that reinforce  each 
other and create a specific perspective by which to interpret the world. It is thus a superclass for Field Frame. Fig. 9 shows the current subclasses of Field Frame and Fig. 10 shows an instance of the Conspiracy Theory field frame modeling the QAnon Field Frame. Although our work is still very tentative, we have already added value to the social science concepts for Climate Obstruction by providing a formal and unified model for three independent informal models. 

![image](https://github.com/user-attachments/assets/a39cd646-ddb2-42a3-a7a1-037bcb1eba1c)

**Figure 9**. Field Frames, Beliefs, and Belief Systems

![image](https://github.com/user-attachments/assets/f33ca7dc-7721-4cd9-8f58-44da6f46a618)

**Figure 10**. An Example Field Frame

![image](https://github.com/user-attachments/assets/2665e810-6a31-4e44-a461-1cd1df4fc9c2)

**Figure 11.** An Example Graph Based on the Model in Figure 5


