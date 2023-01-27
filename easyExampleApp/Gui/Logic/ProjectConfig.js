function projectConfig() {
    return {
        release: {
            app_name: "EasyTexture",
            app_issues_url: "https://github.com/EasyScience/EasyTextureApp/issues"
        },
        tool: {
            poetry: {
                homepage: "https://github.com/EasyScience/EasyTextureApp",
                version: "0.0.1-alpha.1"
            }
        },
        ci: {
            app: {}
        }
    }
}
