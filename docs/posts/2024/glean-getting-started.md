---
title: "Glean Getting Started Guide"
date: 2024-02-12
description: "Step-by-Step guide on how to deploy Glean and get up and running quickly with Enterprise Search and Generative AI."
authors:
  - nathancatania
categories:
  - Glean
  - AI
  - Work
  - Guide
draft: true
comments: false
---

> Any thoughts or opinions in this article are my own and do not reflect those of Glean. I am a Glean SE who worte this guide as part of a project to enhance Glean's documentation and documentation system. This is currently being approved, so in the meantime, the Getting Started guide I wrote is below.

---

## 1.0 - What is Glean?

Glean is a powerful tool designed to streamline your workspace by making information easily accessible. It allows you to search across various data sources, share knowledge with your team, and leverage advanced features for complex workflows.

In addition, Glean provides secure generative AI capabilities, similar to your organization's own dedicated ChatGPT or Bard, but securely trained on your organization's data. This means you don't need to worry about sensitive company data making its way outside the organization.

---

## 2.0 - Access the Glean Admin UI

In this section, you will learn how to access the Glean Administrator User Interface (UI), known as **Workspace Settings**, and begin set up for your organization.

### About the Glean Admin UI
The Glean Admin UI ([app.glean.com/admin](https://app.glean.com/admin)), known as **Workspace Settings**, is where you will manage the Glean workspace for your organization, including setting up Single Sign-On (SSO), configuring data sources, and syncing people data.

### Sign In to Workspace Settings

To access the Workspace Settings for your tenant, navigate to [https://app.glean.com/admin](https://app.glean.com/admin) in your web browser. If you are not already logged in, you will be prompted to do so. Enter your company email address to log in.

![glean-1700136034954-2x](assets/adminui.20240129215320889.webp)

Because we have not configured Single Sign-On (SSO) yet, you will be prompted to check your email for a link to log in. This is called a **Magic Link**. Click the Magic Link in your inbox to log in.

![glean-1700136098518-2x](assets/adminui.20240129215320931.webp)


### Add Additional Administrators

When you sign in for the first time, you will be prompted to add additional administrators before proceeding.

![glean-1700386307365-2x](assets/adminui.20240129215320962.webp)

There are two types of administrator roles, **Admin** and **Setup Admin**:

* The **Admin** role (also known as the **Full Admin** role) has full read/write privileges across all Workspace Settings. This role can add/remove other administrators, manage user permissions, configure data sources, start crawls, and customize the Glean workspace for the organization.
* The **Setup Admin** role has restricted permissions and can only configure data sources and start crawls. This is the perfect role to give to the administrators of any cloud applications that you wish to connect to Glean.

To proceed, enter the emails of any additional administrators that you wish to add, or simply skip to the next step.

!!! warning
    Only select individuals within your organization should be granted provided with the Admin role.

!!! info "Hosting Glean in your own GCP or AWS?"
    You will need to follow the appropriate cloud-prem guide for deploying Glean in GCP or AWS before you can proceed with the rest of this guide.


---

## 3.0 - Configure Single Sign-On (SSO)

![](assets/sso.20240129215322116.webp)

In this section, you will learn how to configure Single Sign-On (SSO) to provide seamless and secure employee access to Glean.

By integrating your directory service with Glean, user information will be automatically synchronized, ensuring that your organization's document access controls are accurately reflected in search results within Glean.

### Understanding Glean SSO
Glean leverages OpenID Connect (OIDC) for implementing SSO and synchronizing directory information. OIDC is a robust protocol that provides detailed control over user permissions. It is widely supported by leading Identity Providers (IdPs) such as Okta, Microsoft Entra ID (Azure AD), and Google, ensuring compatibility and ease of integration with your existing identity management infrastructure.

### Select your Identity Provider (IdP)
On the next screen (under **Setup** > **Authentication**), select your IdP from the list.

![glean-1700456687649-2x](assets/sso.20240129215322149.webp)

Glean also supports the use of SAML in cases where your SSO provider or company company Standard Operating Procedure does not support using OIDC. To configure SAML, please choose **Okta SAML** from the SSO provider list, and paste a link to your IdP metadata XML file when prompted.


!!! warning "OIDC vs SAML"

    Glean strongly recommends the use of OIDC over SAML for integrating SSO. It is crucial that your employee directory is asynchronously reflected within Glean to ensure search functions correctly. SAML tokens do not provide the comprehensive identity data required for Glean's operation, and in addition, can only be updated upon employee re-authentication.

    Should you choose to implement SAML, you will be responsible for maintaining your directory information. This can be done by manually uploading the data to Glean in CSV format or by utilizing Glean's Indexing API to push employee information.


### Configure SSO

Detailed instructions for configuring SSO with each IdP are linked below:

* **TBA**

### Enable SSO

Once you have configured SSO, you will need to tell Glean to switch from using Magic Links to SSO for user and administrator sign-in.

Under the section **Switch to logging into Glean with SSO**, click the **Switch to ...** button.

![glean-1700456650285-2x](assets/sso.20240129215322176.webp)

Your page will refresh, and you will see your IdP listed as **Connected** and **Active**.

![glean-1700456836937-2x](assets/sso.20240129215322204.webp)

!!! info "Heads up!"
    If you don't see the **Switch to ...** button, it means that your Glean tenant is still provisioning and you will not be able to make the switch just yet.

    You can skip ahead to the Connect Your Datasources section and return to this point later.

### Test SSO

There are two key phases of SSO to test: The Glean (SP) to IdP redirect, and the IdP back to Glean redirect.

#### Glean to IdP

To test your SSO configuration, open a new Incognito or **Private Browsing** window and navigate to [https://app.glean.com](https://app.glean.com). Enter your work email and click **Log In**.

You should be redirected to your SSO platform successfully.

??? Danger "Having issues?"
    If redirection to your SSO platform fails, and you are using OIDC, please contact Glean support.

    If you are using SAML, this indicates that the metadata provided to Glean (such as the Login URL) is incorrect. Please check your metadata and if the issue persists, contact Glean support.

#### IdP to Glean

When you have been redirected to your SSO platform, attempt to sign in. You should be redirected back to Glean and successfully signed in.

??? Danger "Having issues?"
    If you can sign in, but redirection back to Glean fails, check whether **BOTH** of the Authentication URLs provided by Glean for you to enter into your IdP have been set correctly.
    
    For OIDC these are:
    ```
    https://[tenant_name]-be.glean.com/authorization-code/callback?isExtension=1
    https://[tenant_name]-be.glean.com/authorization-code/callback
    ```
    If this does fix the issue, change the order of the URLs. If your issue persists, contact Glean Support.


---

## 4.0 - Sync People Data

![](assets/people-data.20240129215321978.webp)

In this section, you will synchronize your employee directory to Glean to ensure secure and accurate search results. Glean calls this identity information _People Data_.

!!! info "Heads up!"
    You will not be able to complete this step until your Glean tenant has been provisioned.
    If you were not able to switch from Magic Links to SSO in the last section, you will need to return to this step later.


### About People Data
Synchronizing your employee directory to Glean is a critical part of the setup process, as it allows Glean to:

* Enforce document permissions.
* Apply role-based access controls (RBAC).
* Deliver more relevant search results.

!!! tip
    If you configured SSO using OIDC in the last step, and your directory is the same as your SSO platform (e.g. Azure AD/Entra ID, Okta), then you have already configured people data sync as part of the SSO configuration, and now simply need to enable it.


### Configure a People Data Source

!!! warning "Using SAML or a People Data source not listed?"
    You will need to manually upload your directory data to Glean. Click here for more information.

Navigate to **Workspace settings** > **Setup** > **People data**.

If your SSO platform supports directory synchronization, it will be listed here with a green checkmark and status **Ready to sync**. Click the SSO provider's icon to proceed.

![glean-1700460408766-2x](assets/people-data.20240129215322021.webp)

If you wish to set up an alternative source, click the appropriate service and follow the setup instructions. If your data source is not listed, please contact Glean support.

#### Attribute Mapping

On the next screen, and if your People Data source supports it, you will be able to map attributes from your directory to the required field in Glean. This is useful if you store user information differently than what is standard.

For example, you might want to infer a user’s location from their manager’s location. If they have an Okta field called `managerLocation`, you could map `managerLocation` to the Glean attribute `location`.

If your People Data source does not support custom mapping in the Glean interface, you will not see this option. Please contact Glean support if you require this feature but do not see it for your configured People Data source.



### Initiate the sync

Before you start the sync, you can preview what information will included. For example, how many users will be created, and how many departments you have. If this is different from what you expected, check that you have provided the correct permissions within the People Data source.

Click **Start sync** to begin synchronization. From this point onwards, the sync is automatic: Glean will check your People Data source periodically for any changes.

![glean-1700461946880-2x](assets/people-data.20240129215322050.webp)

---

## 5.0 - Connect your Datasources

![](assets/datasources.20240129215321504.webp)

In this section, you will learn how to connect the sources of data that Glean will crawl and index for search.


### About Datasources and Connectors

#### Datasources
**Datasources** are the platforms, services, or cloud apps where your data resides. These could be:

| Category | Example Apps                                 |
| -------------- | --------------------------------------------- |
| Cloud Storage   | Box, OneDrive             |
| Email    | Outlook, Gmail            |
| Communication        | Slack, Teams    |
| Documentation        | Confluence, Docusign |
| Ticketing & Support   | Jira, Zendesk      |
| Code & Engineering   | GitHub, BitBucket     |
| HR   | Workday, Lattice     |
| Sales & Marketing   | Salesforce, Marketo     |
| Project Management  | Asana, Monday     |
| [...and more!](https://www.glean.com/connectors)  |     |

#### Connectors
**Connectors** are the tools that Glean uses to connect to your datasources and crawl data from them. Today, Glean supports 80+ connectors to different data sources.

Connectors typically pull data from your datasources securely over API, but may also receive data from your datasources via a webhook.

### Select a Datasource to Connect

From the Glean UI, navigate to [Workspace Settings > Setup > Apps](https://app.glean.com/admin/setup/apps) and click the **Add app** button at the top-right.

![glean-1700789248269-2x](assets/datasources.20240129215321533.webp)

Select the datasource that you want to connect Glean to and follow the instructions that are presented on-screen.

![glean-1700873802158-2x](assets/datasources.20240129215321562.webp)

Connector configuration is typically achieved via OAuth and/or via installing Glean via your cloud app's marketplace/store (e.g. Atlassian Marketplace).

As part of the setup flow for each connector, your API credentials and permissions will be validated.

!!! warning "Error prevention"
    You must apply any API access permissions in the setup documents **exactly** as referenced.
    
    For each item within a datasource, Glean will crawl 3 things:
    
    1. The item itself (ie: spreadsheet, document, message, email, event, etc)
    2. Access permissions for the item (ie: which users have access to the item)
    3. Activities performed on the item (ie: when was the item created/posted/modified/viewed/etc and by which users?)
    
    Glean only asks for the most minimal permissions to perform the above, however, this varies between datasources based on the capabilities of the API provided by the cloud service. For example: Some cloud services only expose document permissions via `ReadWrite` or `FullControl`, instead of a `ReadOnly` API scope.
    
    **Failure to set the correct API access permissions will cause your Glean crawl to fail.**


### Start Crawling
Once you have connected your datasource, you can initiate the crawl for it. This is the process where Glean goes through the data in your connected datasources and indexes it for search.

!!! info
    You will not be able to complete this step until your Glean tenant has been provisioned. If you were not able to switch from Magic Links to SSO in the last section, you will need to return to this step later.

!!! warning
    If you would like to restrict the content that Glean crawls, **DO NOT start crawling**. Crawling restrictions can be applied from [Workspace Settings > Setup > Apps](https://app.glean.com/admin/setup/apps) once the initial configuration for the datasource has been saved.
    
    The restrictions that are supported vary between apps, but most datasources support at least two of the following restrictions:
    
    1. Time-based restrictions (eg: Only crawl created or accessed in the last 6 months)
    2. User-based restrictions (eg: Only crawl content from the specified users)
    3. Group-based restrictions (eg: Only crawl content from the specified AD group)
    4. Site/channel-based restrictions (eg: Only crawl content from the specified site or channel)
    5. Folder-based restrictions (eg: Only crawl content from within the specified folders)
    
    For most apps, greenlisting (explicit inclusion), and redlisting (explicit exclusion) are typically both supported.

    Not all crawling restrictions are available in the UI: some can only be applied by Glean. Contact your Glean account team or Glean support for additional information.





To start the crawl, click on the **Start crawl** button.

You can also start the crawl later by selecting the app under [Workspace Settings > Setup > Apps](https://app.glean.com/admin/setup/apps), and selecting **Start crawl**.

![glean-1700878392608-2x](assets/datasources.20240129215321592.webp)

!!! tip "How long will a crawl take?"
    The initial crawl for any datasource will always take a while; the total time of which is dependent on two key factors:
    
    1. The size of the datasource (eg: number of documents/messages, and the size of each).
    2. The rate limit of the datasource's API.
    
    If an API has a low rate limit, this will affect how quickly Glean can crawl it for items. Likewise, datasources containing a large number of documents, files, or messages, will also take longer to crawl.
    
    For a typical enterprise datasource, expect the initial crawl to take anywhere from 3 days, up to 10 days for large datasources with low API rate limits.



### Checking the Crawl Status

You can check the status of your crawl at any time by going to [Workspace Settings > Setup > Apps](https://app.glean.com/admin/setup/apps) and reviewing the table of configured apps.

Here, you will see information about the progress of the crawl, including how many documents have been indexed and any errors that may have occurred.

![glean-1700876245644-2x](assets/datasources.20240129215321623.webp)

!!! tip
    For crawls of large datasources, or datasources with low rate limits, it is normal for the document count to be low initially and then exponentially increase over a few days.

    If the document count remains low after a few days, please check the permissions granted to the Glean connector and contact Glean support.


### FAQ

See **TBA** for a list of common questions and answers regarding crawling.


---

