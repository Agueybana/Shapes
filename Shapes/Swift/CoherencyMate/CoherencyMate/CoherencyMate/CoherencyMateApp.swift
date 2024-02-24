//
//  CoherencyMateApp.swift
//  CoherencyMate
//
//  Created by Gabriel Suarez on 11/1/23.
//

import SwiftUI

@main
struct CoherencyMateApp: App {
    let persistenceController = PersistenceController.shared

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.managedObjectContext, persistenceController.container.viewContext)
        }
    }
}
