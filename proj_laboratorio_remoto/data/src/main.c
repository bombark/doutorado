/**
 * Copyright (C) 2024  Felipe Bombardelli <felipebombardelli@gmail.com>
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published
 * by the Free Software Foundation, either version 3 of the License, or
 * any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 * 
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

// ============================================================================
//  Header
// ============================================================================

#include <stdio.h>
#include <stdlib.h>
#include <ufr.h>

// ============================================================================
//  main
// ============================================================================

int main() {
    link_t server = ufr_server("@new zmq:socket @host 127.0.0.1 @coder msgpack:obj");

    link_t camera_sub = ufr_sys_subscriber("camera", "@new mqtt:topic @host 185.209.160.8 @topic teste @coder msgpack:obj");

    char buffer[1024*1024];
    while(1) {

        if ( lt_recv_async(&camera_sub) ) {
            size_t bytes = ufr_read(&camera_sub, &buffer[0], sizeof(buffer));
            printf("recebido %ld\n", bytes);
        }
    }
    return 0;
}