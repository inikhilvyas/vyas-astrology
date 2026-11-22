plugins {
    id("com.android.application")
}

android {
    namespace = "in.vyasastro.app"
    compileSdk = 34

    defaultConfig {
        applicationId = "in.vyasastro.app"
        minSdk = 24
        targetSdk = 34
        versionCode = 100
        versionName = "1.0.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        vectorDrawables {
            useSupportLibrary = true
        }
    }

    signingConfigs {
        create("release") {
            // Can be populated via gradle.properties or environment variables
            val keystoreFile = project.rootProject.file("vyas_astra_release.keystore")
            if (keystoreFile.exists()) {
                storeFile = keystoreFile
                storePassword = System.getenv("KEYSTORE_PASSWORD") ?: "vyasastro2026"
                keyAlias = System.getenv("KEY_ALIAS") ?: "vyasastra"
                keyPassword = System.getenv("KEY_PASSWORD") ?: "vyasastro2026"
            }
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
            signingConfig = signingConfigs.getByName("release")
        }
        debug {
            applicationIdSuffix = ".debug"
            isDebuggable = true
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
}

dependencies {
    implementation("androidx.appcompat:appcompat:1.6.1")
    implementation("com.google.android.material:material:1.11.0")
    implementation("androidx.core:core-splashscreen:1.0.1")
    implementation("androidx.webkit:webkit:1.10.0")
    implementation("androidx.activity:activity:1.8.2")
    implementation("androidx.security:security-crypto:1.1.0-alpha06")
}
