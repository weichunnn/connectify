import {
  Box,
  Heading,
  Center,
  Text,
  Button,
  VStack,
  HStack,
  Skeleton,
} from "@chakra-ui/react";
import { ArrowForwardIcon } from "@chakra-ui/icons";

import { useState, useEffect } from "react";
import Navbar from "../components/Navbar";
export default function Feed() {
  const [users, setUsers] = useState([]);
  const comments = [
    "Listening to this in this Hackathon is wild !!!!",
    "I think people who enjoyed retro would enjoy my playlist",
    "Let's talk if you like countries",
    "I think you would like my playlist",
  ];

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
      <Center w="100vw">
        <VStack>
          <Heading fontSize={"6xl"}>
            Feed <br />
          </Heading>
          {users.length > 0 ? (
            users.slice(0, 10).map((user, index) => {
              return (
                <HStack justifyContent={"spaced-between"} w="750px">
                  <Box
                    key={index}
                    w={"full"}
                    boxShadow={"2xl"}
                    rounded={"md"}
                    p={6}
                  >
                    <Text fontSize={"5xl"}>
                      {users[Math.floor(Math.random() * users.length)].name}
                    </Text>
                    <Text color={"gray.200"} fontSize="xl">
                      {comments[Math.floor(Math.random() * comments.length)]}
                    </Text>
                  </Box>
                  <Button
                    rightIcon={<ArrowForwardIcon />}
                    colorScheme="teal"
                    variant="outline"
                    px="10"
                    onClick={() => {
                      window.open(
                        "https://open.spotify.com/playlist/2MAWmLOjIVRd786jKAD3dr"
                      );
                    }}
                  >
                    Let's chat
                  </Button>
                </HStack>
              );
            })
          ) : (
            <VStack spacing="10">
              <Skeleton
                height="150px"
                width={"1000px"}
                color="white"
                rounded="lg"
              />
              <Skeleton
                height="150px"
                width={"1000px"}
                color="white"
                rounded="lg"
              />
              <Skeleton
                height="150px"
                width={"1000px"}
                color="white"
                rounded="lg"
              />
              <Skeleton
                height="150px"
                width={"1000px"}
                color="white"
                rounded="lg"
              />
              <Skeleton
                height="150px"
                width={"1000px"}
                color="white"
                rounded="lg"
              />
              <Skeleton
                height="150px"
                width={"1000px"}
                color="white"
                rounded="lg"
              />
              <Skeleton
                height="150px"
                width={"1000px"}
                color="white"
                rounded="lg"
              />
            </VStack>
          )}
        </VStack>
      </Center>
    </>
  );
}
