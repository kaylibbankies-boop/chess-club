import java.util.*;
import java.time.LocalDateTime;

/**
 * Chess Club Ranking Engine
 *
 * Implements the ranking algorithm for chess club member rankings.
 * This class provides methods to calculate rank changes after matches
 * and validate ranking consistency.
 */
public class RankingEngine {

    /**
     * Represents a chess club member with ranking information
     */
    public static class Member {
        private int id;
        private String name;
        private String surname;
        private int currentRank;
        private int gamesPlayed;

        public Member(int id, String name, String surname, int currentRank, int gamesPlayed) {
            this.id = id;
            this.name = name;
            this.surname = surname;
            this.currentRank = currentRank;
            this.gamesPlayed = gamesPlayed;
        }

        public int getId() { return id; }
        public String getName() { return name; }
        public String getSurname() { return surname; }
        public String getFullName() { return name + " " + surname; }
        public int getCurrentRank() { return currentRank; }
        public int getGamesPlayed() { return gamesPlayed; }

        public void setCurrentRank(int rank) { this.currentRank = rank; }
        public void incrementGamesPlayed() { this.gamesPlayed++; }

        @Override
        public String toString() {
            return String.format("Member{id=%d, name='%s', rank=%d, games=%d}",
                    id, getFullName(), currentRank, gamesPlayed);
        }
    }

    /**
     * Represents the result of a chess match
     */
    public static class MatchResult {
        public enum Result { PLAYER1_WIN, PLAYER2_WIN, DRAW }

        private int player1Id;
        private int player2Id;
        private Result result;
        private LocalDateTime matchDate;
        private String notes;

        public MatchResult(int player1Id, int player2Id, Result result) {
            this(player1Id, player2Id, result, LocalDateTime.now(), null);
        }

        public MatchResult(int player1Id, int player2Id, Result result, LocalDateTime matchDate, String notes) {
            this.player1Id = player1Id;
            this.player2Id = player2Id;
            this.result = result;
            this.matchDate = matchDate;
            this.notes = notes;
        }

        public int getPlayer1Id() { return player1Id; }
        public int getPlayer2Id() { return player2Id; }
        public Result getResult() { return result; }
        public LocalDateTime getMatchDate() { return matchDate; }
        public String getNotes() { return notes; }
    }

    /**
     * Represents the rank changes after a match
     */
    public static class RankChanges {
        private int player1OldRank;
        private int player1NewRank;
        private int player2OldRank;
        private int player2NewRank;

        public RankChanges(int p1Old, int p1New, int p2Old, int p2New) {
            this.player1OldRank = p1Old;
            this.player1NewRank = p1New;
            this.player2OldRank = p2Old;
            this.player2NewRank = p2New;
        }

        public int getPlayer1OldRank() { return player1OldRank; }
        public int getPlayer1NewRank() { return player1NewRank; }
        public int getPlayer2OldRank() { return player2OldRank; }
        public int getPlayer2NewRank() { return player2NewRank; }

        public int getPlayer1Change() { return player1NewRank - player1OldRank; }
        public int getPlayer2Change() { return player2NewRank - player2OldRank; }

        @Override
        public String toString() {
            return String.format("RankChanges{P1: %d→%d (%+d), P2: %d→%d (%+d)}",
                    player1OldRank, player1NewRank, getPlayer1Change(),
                    player2OldRank, player2NewRank, getPlayer2Change());
        }
    }

    /**
     * Calculates rank changes after a match according to the chess club ranking rules
     *
     * Rules:
     * 1. If the higher-ranked player wins, no rank changes occur
     * 2. If the match is a draw:
     *    - If players are not adjacent in ranking, the lower-ranked player gains one position
     *    - If players are adjacent, no changes occur
     * 3. If the lower-ranked player wins against a higher-ranked player:
     *    - The higher-ranked player drops one position
     *    - The lower-ranked player gains floor(rank_difference/2) positions
     *
     * @param player1 The first player
     * @param player2 The second player
     * @param result The match result
     * @return RankChanges object containing the new ranks
     */
    public static RankChanges calculateRankChanges(Member player1, Member player2, MatchResult.Result result) {
        if (player1.getId() == player2.getId()) {
            throw new IllegalArgumentException("Players cannot play against themselves");
        }

        int p1Rank = player1.getCurrentRank();
        int p2Rank = player2.getCurrentRank();

        // Determine higher and lower ranked players
        Member higherRanked, lowerRanked;
        boolean p1IsHigher;

        if (p1Rank < p2Rank) {
            higherRanked = player1;
            lowerRanked = player2;
            p1IsHigher = true;
        } else {
            higherRanked = player2;
            lowerRanked = player1;
            p1IsHigher = false;
        }

        int rankDifference = Math.abs(p1Rank - p2Rank);
        int p1NewRank = p1Rank;
        int p2NewRank = p2Rank;

        switch (result) {
            case DRAW:
                // Draw scenario: lower-ranked player gains position (unless adjacent)
                if (rankDifference > 1) {
                    if (p1IsHigher) {
                        p2NewRank = lowerRanked.getCurrentRank() - 1;
                    } else {
                        p1NewRank = lowerRanked.getCurrentRank() - 1;
                    }
                }
                // If adjacent ranks, no change
                break;

            case PLAYER1_WIN:
                if (p1IsHigher) {
                    // Higher-ranked player wins: no change
                } else {
                    // Lower-ranked player wins against higher-ranked player
                    p2NewRank = higherRanked.getCurrentRank() + 1; // Higher-ranked drops one position
                    int rankGain = rankDifference / 2; // Floor division
                    p1NewRank = lowerRanked.getCurrentRank() - rankGain; // Lower-ranked gains positions
                }
                break;

            case PLAYER2_WIN:
                if (!p1IsHigher) {
                    // Higher-ranked player wins: no change
                } else {
                    // Lower-ranked player wins against higher-ranked player
                    p1NewRank = higherRanked.getCurrentRank() + 1; // Higher-ranked drops one position
                    int rankGain = rankDifference / 2; // Floor division
                    p2NewRank = lowerRanked.getCurrentRank() - rankGain; // Lower-ranked gains positions
                }
                break;
        }

        return new RankChanges(p1Rank, p1NewRank, p2Rank, p2NewRank);
    }

    /**
     * Validates that a set of ranks is consistent (no duplicates, starts from 1, consecutive)
     *
     * @param ranks List of current ranks
     * @return true if ranks are valid, false otherwise
     */
    public static boolean validateRankConsistency(List<Integer> ranks) {
        if (ranks == null || ranks.isEmpty()) {
            return false;
        }

        Set<Integer> uniqueRanks = new HashSet<>(ranks);
        if (uniqueRanks.size() != ranks.size()) {
            return false; // Duplicate ranks found
        }

        Collections.sort(ranks);
        for (int i = 0; i < ranks.size(); i++) {
            if (ranks.get(i) != i + 1) {
                return false; // Not consecutive starting from 1
            }
        }

        return true;
    }

    /**
     * Re-ranks members to ensure consecutive ranking starting from 1
     * This is useful after member deletions or other operations that might
     * create gaps in the ranking
     *
     * @param members List of members to re-rank
     */
    public static void reRankMembers(List<Member> members) {
        // Sort by current rank
        members.sort(Comparator.comparingInt(Member::getCurrentRank));

        // Reassign consecutive ranks
        for (int i = 0; i < members.size(); i++) {
            members.get(i).setCurrentRank(i + 1);
        }
    }

    /**
     * Calculates the expected rank change for a match based on current rankings
     * This can be used for match prediction or difficulty assessment
     *
     * @param player1Rank Current rank of player 1
     * @param player2Rank Current rank of player 2
     * @return Expected rank change (positive means player1 gains, negative means player2 gains)
     */
    public static double calculateExpectedRankChange(int player1Rank, int player2Rank) {
        // Simple ELO-like calculation for expected outcome
        // Higher rank number = lower skill (worse rank)
        double rating1 = 2000.0 / player1Rank; // Convert rank to rating
        double rating2 = 2000.0 / player2Rank;

        double expectedScore1 = 1.0 / (1.0 + Math.pow(10, (rating2 - rating1) / 400.0));
        double expectedScore2 = 1.0 - expectedScore1;

        // Expected rank change (simplified)
        return (expectedScore1 - 0.5) * 2; // Scale to reasonable range
    }

    /**
     * Simulates a tournament round and returns all rank changes
     *
     * @param members List of all members
     * @param matches List of matches in this round
     * @return Map of member IDs to their rank changes
     */
    public static Map<Integer, RankChanges> simulateRound(List<Member> members, List<MatchResult> matches) {
        Map<Integer, Member> memberMap = new HashMap<>();
        for (Member member : members) {
            memberMap.put(member.getId(), new Member(
                member.getId(), member.getName(), member.getSurname(),
                member.getCurrentRank(), member.getGamesPlayed()
            ));
        }

        Map<Integer, RankChanges> allChanges = new HashMap<>();

        for (MatchResult match : matches) {
            Member p1 = memberMap.get(match.getPlayer1Id());
            Member p2 = memberMap.get(match.getPlayer2Id());

            if (p1 == null || p2 == null) {
                throw new IllegalArgumentException("Match references unknown player");
            }

            RankChanges changes = calculateRankChanges(p1, p2, match.getResult());

            // Update ranks for next calculations
            p1.setCurrentRank(changes.getPlayer1NewRank());
            p2.setCurrentRank(changes.getPlayer2NewRank());

            allChanges.put(p1.getId(), changes);
            allChanges.put(p2.getId(), changes);

            // Increment games played
            p1.incrementGamesPlayed();
            p2.incrementGamesPlayed();
        }

        return allChanges;
    }

    /**
     * Main method for testing the ranking engine
     */
    public static void main(String[] args) {
        // Create test members
        List<Member> members = Arrays.asList(
            new Member(1, "Alice", "Smith", 1, 10),
            new Member(2, "Bob", "Johnson", 2, 8),
            new Member(3, "Charlie", "Brown", 3, 6),
            new Member(4, "Diana", "Wilson", 4, 4)
        );

        System.out.println("Initial Rankings:");
        members.forEach(System.out::println);

        // Test rank changes calculation
        System.out.println("\nTesting rank changes:");

        // Higher ranked wins (no change)
        RankChanges changes1 = calculateRankChanges(members.get(0), members.get(1), MatchResult.Result.PLAYER1_WIN);
        System.out.println("Alice (rank 1) beats Bob (rank 2): " + changes1);

        // Lower ranked wins
        RankChanges changes2 = calculateRankChanges(members.get(1), members.get(0), MatchResult.Result.PLAYER1_WIN);
        System.out.println("Bob (rank 2) beats Alice (rank 1): " + changes2);

        // Draw between non-adjacent players
        RankChanges changes3 = calculateRankChanges(members.get(0), members.get(2), MatchResult.Result.DRAW);
        System.out.println("Alice (rank 1) draws Charlie (rank 3): " + changes3);

        // Draw between adjacent players
        RankChanges changes4 = calculateRankChanges(members.get(1), members.get(2), MatchResult.Result.DRAW);
        System.out.println("Bob (rank 2) draws Charlie (rank 3): " + changes4);

        // Validate rank consistency
        List<Integer> ranks = Arrays.asList(1, 2, 3, 4);
        System.out.println("\nRank consistency check: " + validateRankConsistency(ranks));

        List<Integer> invalidRanks = Arrays.asList(1, 2, 2, 4);
        System.out.println("Invalid ranks check: " + validateRankConsistency(invalidRanks));
    }
}