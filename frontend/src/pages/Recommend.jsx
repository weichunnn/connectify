import {
  Heading,
  Avatar,
  Box,
  Center,
  Text,
  Stack,
  Button,
  Link,
  Badge,
  Spinner,
  VStack,
  Highlight,
  HStack,
} from "@chakra-ui/react";
import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";

export default function Recommend() {
  const [users, setUsers] = useState([]);
  const [end, setEnd] = useState(false);

  const [index, setIndex] = useState(0);

  useEffect(() => {
    fetch("http://localhost:8080/recommendations", {
      method: "GET",
    })
      .then((res) => res.json())
      .then((data) => {
        setUsers(data.data);
        console.log("data", data);
      });
  }, []);

  return (
    <>
      <Navbar />
      <Center w="100vw" h="80vh">
        {end ? (
          <VStack>
            <Heading>
              Hmm, looks like we found everyone that has a similar taste with
              you.
            </Heading>
            <Heading>Check out the feed for new postings</Heading>
          </VStack>
        ) : (
          <VStack>
            {users.length > 0 ? (
              <>
                <Heading> Here are some people that</Heading>
                <Heading lineHeight="tall">
                  <Highlight
                    query="similar interest"
                    styles={{
                      px: "2",
                      py: "1",
                      rounded: "full",
                      bg: "red.100",
                    }}
                  >
                    we think have similar interest with you
                  </Highlight>
                </Heading>
                <Text fontSize="4xl" fontWeight={"bold"} pt="12" pb="4">
                  My top song choices
                </Text>
                <HStack spacing="40">
                  <VStack>
                    // select either a or base
                    <Avatar
                      size={"xl"}
                      src={
                        Math.random() > 0.5
                          ? "https://xsgames.co/randomusers/avatar.php?g=female"
                          : "https://xsgames.co/randomusers/avatar.php?g=male"
                      }
                      alt={"Avatar Alt"}
                      mb={4}
                      pos={"relative"}
                      _after={{
                        content: '""',
                        w: 4,
                        h: 4,
                        bg: "green.300",
                        border: "2px solid white",
                        rounded: "full",
                        pos: "absolute",
                        bottom: 0,
                        right: 3,
                      }}
                    />
                    <Heading fontSize={"2xl"} fontFamily={"body"}>
                      {users[index].name}
                    </Heading>
                    <Text fontWeight={600} color={"gray.500"} mb={4}>
                      @{users[index].name.toLowerCase().replace(" ", "")}
                    </Text>
                  </VStack>
                  <VStack>
                    {users[index].tracks.map((track) => {
                      return (
                        <Box
                          bg="purple.200"
                          px="10"
                          py="4"
                          rounded={"lg"}
                          color="black"
                        >
                          {track.song_name}
                        </Box>
                      );
                    })}
                  </VStack>
                </HStack>
                <HStack w={"750px"} pt="20">
                  <Button
                    flex={1}
                    colorScheme="red"
                    py="6"
                    onClick={() => {
                      if (index == users.length - 1) {
                        setEnd(true);
                      }
                      setIndex(index + 1);
                    }}
                  >
                    Pass
                  </Button>
                  <Button
                    flex={1}
                    colorScheme="teal"
                    py="6"
                    onClick={() => {
                      if (index == users.length - 1) {
                        setEnd(true);
                      }
                      setIndex(index + 1);
                    }}
                  >
                    Follow
                  </Button>
                </HStack>
              </>
            ) : (
              <VStack alignItems={"center"} justifyContent="center">
                <Spinner size="xl" />
                <Text fontSize="lg" pt="10">
                  Generating recommendations
                </Text>
              </VStack>
            )}
          </VStack>
        )}
      </Center>
    </>
  );
}
