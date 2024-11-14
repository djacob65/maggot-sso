<#-- Extend the parent theme -->
<#import "login.ftl" as parent>

<div id="kc-header-wrapper">
    <div id="kc-logo-title">
        <!-- Add the logo -->
        <img src="${url.resourcesPath}/img/logo.png" alt="Logo" id="kc-logo">

        <!-- Add the title -->
        <h1 id="kc-page-title">${realm.displayNameHtml?:realmName}</h1>
    </div>
</div>