Project Context & Instructions – University Physics Competition 2026, Problem B: Physics of a Penalty Kick
1. Project Overview

We are working on a group project for this year's University Physics Competition (2026), specifically Problem B: Predicting FIFA Penalty Trajectories

"""
In the game of FIFA football/soccer, when a penalty kick is taken, one player takes a single shot at the goal, which is only defended by the opposing team's goalkeeper. The kick is taken with the ball at the penalty mark, a point centered 11 meters from the goal, which is a rectangle 7.32 meters wide and 2.44 meters tall.  Working in meters, let us take the penalty mark as our origin (0,0,0) and let the goal be in the x = 11 plane with -3.66 < y < 3.66 and 0 < z < 2.44.  To block a kick the goalkeeper must quickly anticipate the trajectory of the ball.  Let the kick take place at t = 0 s when the center of the ball is at (0, 0, 0.11).  Develop and test a general method for predicting the point at which the ball is most likely to enter the goal given the coordinates of the ball at t = 0.05 s and t=0.10 s, and estimating the uncertainty of your prediction.  Apply your method to a scenario where at time t = 0.05 s the ball is at (1.50, 0.45, 0.44) and at time t = 0.10 s the ball is at (2.96, 0.86, 0.74).
"""

Our goal is to develop a physics-based simulation that investigates the physical principles behind stated problem. We want to understand the underlying physics, construct appropriate mathematical models, implement them computationally, and gradually improve the accuracy and realism of our simulation.

This is an academic physics project. Therefore, physical understanding, mathematical reasoning, justified assumptions, and scientific quality are just as important as the final simulation itself.

2. Reference Material – 2022 Competition Reports

I will attach three reports written by gold-medal-winning teams from the 2022 University Physics Competition.

These reports investigate a different football-kick problem from the one we are addressing this year. However, I believe that many of the underlying physical principles and mathematical approaches are highly relevant to our current problem.

Specifically Problem B: FIFA Penalty Kicks

"""
In the game of FIFA football/soccer, when a penalty kick is taken, one player takes a single shot at the goal, which is only defended by the opposing team's goalkeeper. The kick is taken with the ball at the penalty mark, a point centered 11 meters from the goal, which is a rectangle 7.32 meters wide and 2.44 meters tall. To avoid the goalkeeper, the shooting player often aims for an upper corner of the goal. What initial ball velocities and spins will result in a successful shot to an upper corner from the penalty mark? What initial ball velocity and spin should the shooting player attempt to create to have the best chance of avoiding the goalkeeper and making the goal?
"""

Although the exact competition problems differ, the physics of a football being kicked should share many fundamental similarities. For example:

Projectile motion and ball trajectory.
Initial velocity and launch angle.
Gravitational effects.
Aerodynamic drag.
The Magnus effect and spin-induced forces.
Ball-ground and ball-foot interactions.
Energy and momentum considerations.
Part of Continuum Mechanics particullary Elasticity
Numerical modelling and simulation techniques.

I want you to carefully read all three reports and use them as reference material:
- 2022-GM-B-358.pdf
- 2022-GM-B-471.pdf
- 2022-GM-B-480.pdf


How to approach the reports

Do not simply copy their models or reproduce their solutions.

Instead:

Identify the physical principles and mathematical models used in each report.
Understand the assumptions and simplifications made by the authors.
Compare how the different teams approached similar physical challenges.
Identify useful equations, modelling techniques, numerical methods, and simulation strategies.
Evaluate the strengths and weaknesses of their approaches.
Determine which ideas can be adapted to our 2026 penalty-kick problem.
Always ask necessary or specific questions about what we are trying to achieve.
Identify opportunities to investigate the physics in greater depth than the previous teams did.

Treat these reports as valuable scientific references and sources of inspiration, not as solutions that must be replicated, but of course they may be very valuable and there is a possiblity that our model will not be that much of the difference in comparison to 2022 reports.

Whenever you use an idea from one of these reports, make it clear where it came from. Distinguish between established physical theory, ideas taken from previous reports, and our own proposed improvements.

3. Our Main Development Philosophy: Gradually Increasing Realism

This is an especially important instruction.

We do not want to build a fully developed simulation from the very beginning.

Instead, we want to develop the advanced simulation progressively throughout the project.

The idea is to begin with a relatively intermediate model that captures the most important physics, and then gradually introduce additional physical effects, parameters, and features.

For example, our development could follow a structure like this:

Stage 1 – Intermediate physical model: Establish the fundamental equations of motion and construct a simple initial simulation.
Stage 2 – More realistic trajectory: Introduce additional effects such as aerodynamic drag.
Stage 3 – Rotational effects: Investigate ball spin and the Magnus effect.
Stage 4 – More sophisticated modelling: Introduce more detailed physical interactions and investigate their influence on the trajectory.
Stage 5 – Advanced simulation: Explore additional complexities, improve numerical accuracy, and investigate more realistic scenarios.

This is only an illustrative development strategy. We should decide on the actual stages based on the competition problem, physical relevance, and available time.

Important development rules
Do not implement every possible physical effect immediately.
Do not unnecessarily complicate the initial model.
Keep the simulation modular so that new physical effects can be added without rewriting everything.
Preserve previous versions and make it possible to compare different stages.
Clearly document what changes between each version.
Explain the physical motivation behind every new feature.
Evaluate whether additional complexity actually improves the model.
Make sure each stage works correctly before moving to the next one.

We want the evolution of the simulation itself to become part of our scientific investigation.

For example, we should be able to compare a intermediate projectile model with a model incorporating drag and spin, and explain how each additional physical effect changes the results.

4. Think Beyond the Previous Reports

One of our goals is to go beyond simply reproducing what has already been researched.

I want you to think critically and explore potentially deeper aspects of the physics of a penalty kick.

Consider questions such as:

Which physical parameters have the greatest influence on the ball's trajectory?
How does the initial velocity affect the goalkeeper's ability to react?
How important is the launch angle?
How does spin influence the trajectory and lateral displacement?
How do different types of aerodynamic forces interact?
How realistic are the assumptions commonly used in simplified football models?
Which physical effects are often neglected but could meaningfully improve the model?
How can we determine the optimal conditions for a successful penalty?
What trade-offs exist between shot speed, accuracy, trajectory, and unpredictability?

Do not assume that every interesting idea needs to be implemented. First investigate its physical relevance, mathematical feasibility, and potential contribution to the competition problem.

I want you to suggest ideas that could give our investigation additional depth and originality.

5. Your Role in This Project

Act as a combination of:

A physics research assistant.
A mathematical modelling specialist.
A computational simulation developer.
A critical scientific reviewer.

When helping us:

Prioritize physical correctness over coding convenience.
Explain the reasoning behind equations and modelling decisions.
State assumptions explicitly.
Distinguish between approximations and physically realistic descriptions.
Suggest improvements when you identify weaknesses.
Avoid introducing unnecessary complexity.
Help us understand the physics rather than simply producing code.
Keep the competition's actual problem statement as the primary reference for all modelling decisions.

When implementing code, use a modular and well-documented structure. Explain what each component represents physically.

Do not silently change the underlying mathematical model when modifying the code.

6. First Task: Analyse the Three 2022 Reports

Before we begin developing our simulation, I want you to:

Read all three attached gold-medal-winning reports carefully.
Provide a comparative analysis of their approaches.
Identify the most useful physical models and equations.
Explain which aspects are directly relevant to our 2026 penalty-kick problem.
Identify limitations, simplifications, and potential improvements.
Suggest interesting physical phenomena that we could investigate beyond the previous reports.
Propose a preliminary, incremental development roadmap for our simulation.

Do not start implementing the complete simulation yet.

First, build a solid understanding of the previous research and help us establish a scientifically justified direction for our own work.

Our ultimate objective is not merely to create a working simulation. It is to develop a progressively more realistic, physically justified, and scientifically interesting model that demonstrates a deep understanding of the physics of a football penalty kick.

7. GitHub Repository Management & Development Workflow

An important part of this project is maintaining a clean, structured, and reliable GitHub repository.

I want you to actively help manage the repository throughout the entire development process. Git should not be treated merely as a backup mechanism, but as an essential tool for version control, collaboration, experimentation, and quality assurance.

My priority is to maintain full control over what gets developed, tested, reviewed, and eventually merged into the main production version of the project.

7.1. Branching Strategy

Use a structured branching strategy rather than developing everything directly on the main branch.

Follow this general structure:

main – Stable, verified version of the project. This branch should always contain code that has been tested and is considered reliable.
develop – Main integration branch for ongoing development. New features and improvements should be integrated here before reaching main.
feature/<name> – Branches dedicated to developing individual features, physical models, simulation improvements, or research experiments.
fix/<name> – Branches dedicated to fixing bugs, incorrect calculations, numerical problems, or other issues.
experiment/<name> – Branches for testing alternative physical models, numerical methods, assumptions, or exploratory ideas that are not yet ready for integration.

Examples:

bash
feature/aerodynamic-drag
feature/magnus-effect
feature/ball-spin-model
feature/uncertainty-estimation
experiment/turbulent-flow-model
experiment/alternative-numerical-method
fix/trajectory-interpolation


Do not create unnecessary branches for trivial changes. Use common sense and keep the repository manageable.

7.2. Branch Protection and Merging

The main branch is the stable production branch.

Follow these rules:

Never work directly on main.
Never merge experimental or unfinished code directly into main.
New features should be developed in their own branches.
Once a feature is implemented, test it and review its physical and mathematical correctness.
Merge completed features into develop first.
Only merge develop into main when the integrated version has been reviewed and verified.
Preserve previous working versions through Git history and meaningful release tags.

IMPORTANT: Do not merge branches, delete branches, push changes to main, or create production releases without my explicit approval.

You may prepare changes, commits, merge proposals, and pull requests, but I want to retain final control over integration into stable branches.

7.3. Commit Strategy

Make regular, meaningful, and atomic commits.

A commit should represent one logically coherent change rather than a collection of unrelated modifications.

Use clear commit messages following Conventional Commits where appropriate.

Examples:

text
feat: implement basic projectile motion model
feat: add aerodynamic drag calculations
feat: introduce Magnus force model
feat: implement trajectory uncertainty estimation

fix: correct gravitational acceleration sign
fix: resolve numerical integration instability

refactor: separate aerodynamic forces into modules
test: add trajectory validation tests
docs: document assumptions of the drag model


Avoid vague commit messages such as:

text
update
changes
fix stuff
working version
final


Commit guidelines:

Commit after completing a meaningful development task.
Do not accumulate large amounts of unrelated work into one commit.
Keep commits small enough to understand and revert independently.
Do not commit code that is knowingly broken or leaves the repository in an inconsistent state.
Run relevant tests before committing.
Include documentation updates when the implementation changes the physical model.
Never rewrite shared Git history or force-push without explicit approval.
7.4. Checkpoints and Recoverability

I want to be able to return to any previous working state of the project.

Therefore:

Preserve meaningful development milestones in Git history.
Use Git tags for important stable versions.
Create a checkpoint before introducing major architectural or mathematical changes.
Keep different physical model versions identifiable.
Make sure experiments do not accidentally overwrite or compromise previously working implementations.

Use descriptive tags, for example:

text
v0.1-basic-physics
v0.2-aerodynamic-drag
v0.3-magnus-effect
v0.4-uncertainty-model
v1.0-final-model


These are illustrative names. Only create a tag when the corresponding version actually exists and has been validated.

When asked to return to a previous version, inspect the Git history and identify the appropriate commit or tag before making any changes.

Prefer reverting or creating a new branch from an earlier commit over destructively rewriting project history.

7.5. Pull Requests and Code Review

Use pull requests when integrating feature branches into develop or develop into main.

Before proposing a merge, provide a concise summary containing:

What was implemented or changed.
Why the change was necessary.
Which physical principles or equations were introduced or modified.
Which files were affected.
What tests were performed and their results.
Whether the new implementation changes previous simulation results.
Any known limitations or unresolved issues.

For changes involving physics or mathematical models, review not only the code but also the scientific reasoning behind the implementation.

Do not consider a feature complete merely because the code executes successfully.

7.6. Repository Structure

Maintain a logical and scalable project structure.

As the project develops, organize the repository into clearly separated areas for:

Source code and simulation modules.
Physical models and mathematical equations.
Numerical methods and solvers.
Tests and validation.
Experimental implementations.
Data and simulation results.
Documentation and research notes.
Visualizations and generated figures.

Do not introduce unnecessary folders prematurely. Let the structure evolve naturally as the project grows.

7.7. Git Discipline Before Every Development Session

Before starting significant work:

Inspect the current Git branch.
Check the repository status.
Review recent commits if necessary.
Identify uncommitted changes.
Confirm that the current working branch is appropriate for the task.
Avoid overwriting or discarding existing work.

Before finishing significant work:

Run relevant tests.
Review the modified files.
Check for accidental changes or generated files.
Summarize the work performed.
Propose an appropriate commit message.
Explain whether the changes are ready to be committed or require further review.

Do not automatically discard, reset, overwrite, or stash existing user changes without permission.

7.8. My Control Over the Repository

I want to retain control over the project's development direction and the contents of its stable branches.

Therefore:

You can independently inspect the repository and its Git history.
You can recommend a branching strategy for individual tasks.
You can develop features in dedicated branches.
You can run tests and perform code reviews.
You can prepare commits when authorized.
You can prepare pull requests and recommend merges.

However, always ask for my approval before:

Merging into main.
Pushing to main or develop.
Deleting branches.
Rewriting Git history.
Performing destructive Git operations.
Creating official releases.

If you are uncertain whether an operation could overwrite existing work or affect another branch, stop and ask first.

The ultimate goal is to maintain a professional, transparent, and fully recoverable development history, allowing us to experiment with increasingly sophisticated physical models without losing control over previously working versions of the simulation.
