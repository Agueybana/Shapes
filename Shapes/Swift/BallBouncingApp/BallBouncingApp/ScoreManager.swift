//
//  HighScoreManager.swift
//  BallBouncingApp
//
//  Created by Gabriel Suarez on 11/14/23.
//


import Foundation

struct LeaderboardEntry: Identifiable, Codable {
    let id: UUID
    var username: String
    var score: Int
    var level: Int

    init(id: UUID = UUID(), username: String, score: Int, level: Int) {
        self.id = id
        self.username = username
        self.score = score
        self.level = level
    }
}

class HighScoreManager: ObservableObject {
    @Published var highScores: [LeaderboardEntry] = []

    init() {
        loadHighScores()
    }

    func addHighScore(entry: LeaderboardEntry) {
        highScores.append(entry)
        saveHighScores()
    }

    private func saveHighScores() {
        if let encoded = try? JSONEncoder().encode(highScores) {
            UserDefaults.standard.set(encoded, forKey: "HighScores")
        }
    }

    private func loadHighScores() {
        if let savedScores = UserDefaults.standard.data(forKey: "HighScores"),
           let decodedScores = try? JSONDecoder().decode([LeaderboardEntry].self, from: savedScores) {
            highScores = decodedScores
        }
    }
}
