import requests


print(
    requests.post(
        "http://0.0.0.0:10000",
        json={
            "from_email": "rayfunahashi@gmail.com",
            "content": """
                Dear Dr. Ray,

                My name is Sarah Howard, and I'm the CEO of RetroTech - a startup that is modernizing vintage tech products.

                I wanted to introduce RetroTech because I think we would make an exciting addition to Raven Capital's portfolio.

                As you know, vintage products like record players and Polaroids have seen a major resurgence in popularity lately. RetroTech is capitalizing on this growing nostalgia market by re-engineering classic tech into modern versions with contemporary features.

                For example, our vinyl record player has built-in Bluetooth capabilities so customers can wirelessly play their digitized collection. We also added USB ports for converting records to digital files. Our reinvented Polaroid camera uploads printed photos to the cloud for easy sharing on social media.

                These product upgrades and hybridizations of analog and digital allow RetroTech to deliver the nostalgic appeal people love while providing the connectivity today's consumers expect.

                We already have over 5,000 pre-orders for our record player and camera products launching later this year. With your investment support, we can scale up inventory production, expand our product line into more vintage tech, and disrupt a market valued at over $200 million.

                I would love to schedule a meeting to show you our prototypes and discuss RetroTech's growth roadmap in more detail. Are you available next Tuesday at 11am? I look forward to your reply.

                Best,
                Sarah Howard
                CEO, RetroTech
                sarah@retrotech.com
                555-123-4567
                """
        }
    ).json()
)

