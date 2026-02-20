### Default Work Package Content and Tool Selection Behavior

In *Per Work Package* view mode, the platform distinguishes between **temporal tool selection** and **default content behavior**.

#### Temporal Tool Selection
When a user selects a tool from the secondary (tools) bar and navigates between different Work Packages, the selected tool is preserved. Upon returning to the same Work Package, the previously selected tool is displayed again. This behavior reflects intentional user interaction and is maintained within the active session.

#### Default Content Behavior
In cases of page refresh, re-login, or session reset, no tool is preselected by default. When the user selects a Work Package under these conditions, the platform displays the basic content of the corresponding `wp<number>.py` file in the main content area.

This default content serves as a temporary visual and contextual anchor, ensuring that meaningful information is presented while the intended tool selection logic is recalculated or deferred.

Once a tool is explicitly selected (or preselected in future versions), the tool content replaces the Work Package content in the main content area.

This behavior is designed to provide continuity, clarity, and a smooth transition between contextual and functional views.